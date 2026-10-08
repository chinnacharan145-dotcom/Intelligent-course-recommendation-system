from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Roadmap, RoadmapNode, RoadmapNodeSkill, Action, StudentAction, StudentActionHistory
from .serializers import RoadmapSerializer, RoadmapNodeSerializer, StudentActionSerializer
from apps.students.models import StudentProfile, StudentSkill
from apps.careers.models import CareerSkill

class RoadmapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_or_create_roadmap(self, student_profile):
        primary_goal = student_profile.career_goals.filter(is_primary=True).first()
        if not primary_goal:
            return None, "No primary career goal selected. Please set a primary career goal."

        career = primary_goal.career
        roadmap, created = Roadmap.objects.get_or_create(
            student=student_profile,
            career=career,
            defaults={
                "title": f"Career Roadmap for {career.name}",
                "description": f"Personalized engineering milestone roadmap targeting {career.name}.",
                "status": "ACTIVE"
            }
        )

        if created or not roadmap.nodes.exists():
            # Build initial roadmap nodes from CareerSkills
            req_skills = CareerSkill.objects.filter(career=career).select_related('skill').order_by('required_level', 'importance')
            student_skills_map = {ss.skill_id: ss.proficiency for ss in student_profile.skills.all()}

            completed_nodes = 0
            total_nodes = req_skills.count()

            for idx, req in enumerate(req_skills, start=1):
                curr_lvl = student_skills_map.get(req.skill_id, 0)
                is_done = curr_lvl >= req.required_level
                status_val = RoadmapNode.Status.COMPLETED if is_done else (RoadmapNode.Status.IN_PROGRESS if curr_lvl > 0 else RoadmapNode.Status.NOT_STARTED)
                
                if is_done:
                    completed_nodes += 1

                node = RoadmapNode.objects.create(
                    roadmap=roadmap,
                    skill=req.skill,
                    title=f"Master {req.skill.name} (Level {req.required_level})",
                    description=f"Required target proficiency: Level {req.required_level}. Current proficiency: Level {curr_lvl}.",
                    node_type=RoadmapNode.NodeType.SKILL,
                    sequence_order=idx,
                    status=status_val,
                    progress=100.0 if is_done else (curr_lvl / req.required_level * 100.0 if req.required_level > 0 else 0.0),
                    estimated_hours=req.importance * 5.0
                )
                RoadmapNodeSkill.objects.create(
                    roadmap_node=node,
                    skill=req.skill,
                    target_level=req.required_level
                )

            roadmap.overall_progress = round((completed_nodes / total_nodes * 100.0), 1) if total_nodes > 0 else 100.0
            roadmap.save()

        return roadmap, None

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        roadmap, err = self.get_or_create_roadmap(profile)
        if err:
            return Response({"success": False, "message": err, "data": None}, status=status.HTTP_200_OK)

        serializer = RoadmapSerializer(roadmap)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })


class RoadmapRecalculateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        primary_goal = profile.career_goals.filter(is_primary=True).first()
        if not primary_goal:
            return Response({"success": False, "message": "No primary career goal selected."}, status=status.HTTP_400_BAD_REQUEST)

        # Clear and rebuild roadmap
        Roadmap.objects.filter(student=profile).delete()
        roadmap_view = RoadmapView()
        roadmap, err = roadmap_view.get_or_create_roadmap(profile)

        return Response({
            "success": True,
            "data": RoadmapSerializer(roadmap).data,
            "message": "Roadmap recalculated successfully."
        })


class RoadmapNodeCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        node = get_object_or_404(RoadmapNode, pk=pk, roadmap__student=profile)

        node.status = RoadmapNode.Status.COMPLETED
        node.progress = 100.0
        node.completed_at = timezone.now()
        node.save()

        # Update student skill if node linked to skill
        if node.skill:
            req_skill = RoadmapNodeSkill.objects.filter(roadmap_node=node).first()
            target_lvl = req_skill.target_level if req_skill else 4
            StudentSkill.objects.update_or_create(
                student=profile,
                skill=node.skill,
                defaults={
                    'proficiency': target_lvl,
                    'source': StudentSkill.SourceChoice.MANUAL_OVERRIDE
                }
            )

        # Recalculate roadmap overall progress
        roadmap = node.roadmap
        total_nodes = roadmap.nodes.count()
        completed_nodes = roadmap.nodes.filter(status=RoadmapNode.Status.COMPLETED).count()
        roadmap.overall_progress = round((completed_nodes / total_nodes * 100.0), 1) if total_nodes > 0 else 100.0
        roadmap.save()

        return Response({
            "success": True,
            "data": RoadmapNodeSerializer(node).data,
            "message": "Roadmap node marked as completed!"
        })


class NextBestActionView(APIView):
    """
    Answers the central product question: 'What should I do next?'
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        primary_goal = profile.career_goals.filter(is_primary=True).first()

        if not primary_goal:
            return Response({
                "success": True,
                "data": {
                    "action_title": "Set Your Primary Career Goal",
                    "action_type": "ONBOARDING",
                    "reason": "Select your target engineering career goal to unlock personalized recommendations.",
                    "priority_score": 100.0
                },
                "message": None
            })

        # Find first uncompleted roadmap node
        first_node = RoadmapNode.objects.filter(
            roadmap__student=profile,
            status__in=[RoadmapNode.Status.NOT_STARTED, RoadmapNode.Status.IN_PROGRESS]
        ).order_by('sequence_order').first()

        if first_node:
            return Response({
                "success": True,
                "data": {
                    "action_title": f"Focus on: {first_node.title}",
                    "action_type": "SKILL_ACQUISITION",
                    "node_id": str(first_node.id),
                    "reason": f"This is the next critical skill node for {primary_goal.career.name}.",
                    "priority_score": 95.0
                },
                "message": None
            })

        return Response({
            "success": True,
            "data": {
                "action_title": "Take a Career Practice Assessment",
                "action_type": "ASSESSMENT",
                "reason": "You have completed your primary roadmap nodes! Validate your skills with an assessment.",
                "priority_score": 80.0
            },
            "message": None
        })
