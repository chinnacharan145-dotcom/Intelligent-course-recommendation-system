/**
 * CourseAI - Intelligent Course Recommendation System SPA Frontend Engine
 */

class CourseAIApp {
    constructor() {
        this.apiBase = '/api/v1';
        this.token = localStorage.getItem('access_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
        this.currentView = 'dashboard';
        this.activeQuizAttempt = null;
        this.quizTimer = null;

        this.init();
    }

    async init() {
        this.setupEventListeners();
        
        if (!this.token) {
            this.showAuthModal('login');
        } else {
            await this.loadUserProfile();
            this.renderView(this.getHashView());
        }

        if (window.lucide) {
            lucide.createIcons();
        }
    }

    getHashView() {
        const hash = window.location.hash.replace('#', '');
        return hash || 'dashboard';
    }

    setupEventListeners() {
        // Hash navigation
        window.addEventListener('hashchange', () => {
            this.renderView(this.getHashView());
        });

        // Sidebar clicks
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const view = item.getAttribute('data-view');
                document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
            });
        });

        // Logout
        const btnLogout = document.getElementById('btn-logout');
        if (btnLogout) {
            btnLogout.addEventListener('click', () => this.logout());
        }

        // Onboarding trigger
        const btnOnboarding = document.getElementById('btn-trigger-onboarding');
        if (btnOnboarding) {
            btnOnboarding.addEventListener('click', () => this.renderOnboarding());
        }

        // Modal Close handlers
        document.querySelectorAll('[data-close-modal]').forEach(btn => {
            btn.addEventListener('click', () => {
                const modalId = btn.getAttribute('data-close-modal');
                document.getElementById(modalId)?.classList.add('hidden');
            });
        });
    }

    async apiFetch(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, config);
            const data = await response.json();
            
            if (response.status === 401 && !endpoint.includes('/auth/login/')) {
                this.logout();
                throw new Error("Session expired. Please log in again.");
            }

            return data;
        } catch (err) {
            console.error(`API Error on ${endpoint}:`, err);
            throw err;
        }
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        this.token = null;
        this.user = null;
        this.showAuthModal('login');
    }

    async loadUserProfile() {
        try {
            const res = await this.apiFetch('/auth/me/');
            if (res.success) {
                this.user = res.data;
                localStorage.setItem('user', JSON.stringify(this.user));
                this.updateUserUI();
            }
        } catch (e) {
            console.warn("Could not fetch profile:", e);
        }
    }

    updateUserUI() {
        if (!this.user) return;

        const nameElem = document.getElementById('user-sidebar-name');
        const avatarElem = document.getElementById('user-avatar-initials');
        const navAdmin = document.getElementById('nav-admin');

        if (nameElem) nameElem.textContent = `${this.user.first_name || 'Student'} ${this.user.last_name || ''}`;
        if (avatarElem) {
            const initials = `${(this.user.first_name || 'S')[0]}${(this.user.last_name || 'U')[0]}`.toUpperCase();
            avatarElem.textContent = initials;
        }

        if (navAdmin) {
            if (this.user.role === 'admin' || this.user.is_staff) {
                navAdmin.classList.remove('hidden');
            } else {
                navAdmin.classList.add('hidden');
            }
        }
    }

    renderView(viewName) {
        this.currentView = viewName;
        const container = document.getElementById('view-container');
        const titleElem = document.getElementById('page-title');

        if (!container) return;

        // Update active nav
        document.querySelectorAll('.nav-item').forEach(item => {
            if (item.getAttribute('data-view') === viewName) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        switch (viewName) {
            case 'dashboard':
                if (titleElem) titleElem.textContent = "Student Dashboard";
                this.renderDashboard(container);
                break;
            case 'recommendations':
                if (titleElem) titleElem.textContent = "Course Recommendations";
                this.renderRecommendations(container);
                break;
            case 'roadmap':
                if (titleElem) titleElem.textContent = "Interactive Learning Roadmap";
                this.renderRoadmap(container);
                break;
            case 'skill-gap':
                if (titleElem) titleElem.textContent = "Skill Gap Analysis";
                this.renderSkillGap(container);
                break;
            case 'careers':
                if (titleElem) titleElem.textContent = "Career Explorer";
                this.renderCareers(container);
                break;
            case 'assessments':
                if (titleElem) titleElem.textContent = "Skill Assessments";
                this.renderAssessments(container);
                break;
            case 'courses':
                if (titleElem) titleElem.textContent = "Course Catalog";
                this.renderCourses(container);
                break;
            case 'profile':
                if (titleElem) titleElem.textContent = "Student Profile";
                this.renderProfile(container);
                break;
            case 'admin':
                if (titleElem) titleElem.textContent = "Admin Analytics Portal";
                this.renderAdmin(container);
                break;
            default:
                this.renderDashboard(container);
        }

        if (window.lucide) lucide.createIcons();
    }

    /* ---------------- 1. DASHBOARD VIEW ---------------- */
    async renderDashboard(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Loading Dashboard Data...</p></div>`;

        try {
            const res = await this.apiFetch('/dashboard/');
            if (!res.success) throw new Error(res.message);

            const d = res.data;

            container.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon blue"><i data-lucide="target"></i></div>
                        <div class="stat-info">
                            <div class="label">Career Readiness</div>
                            <div class="value">${d.career_readiness}%</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon emerald"><i data-lucide="check-circle-2"></i></div>
                        <div class="stat-info">
                            <div class="label">Profile Completion</div>
                            <div class="value">${d.profile_completion}%</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon purple"><i data-lucide="award"></i></div>
                        <div class="stat-info">
                            <div class="label">Skills Acquired</div>
                            <div class="value">${d.skills_count}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon amber"><i data-lucide="book-open"></i></div>
                        <div class="stat-info">
                            <div class="label">Courses Completed</div>
                            <div class="value">${d.completed_courses_count}</div>
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <h2><i data-lucide="sparkles" style="color: var(--accent-cyan)"></i> Top Recommendations</h2>
                            <button class="btn btn-outline" id="btn-dashboard-refresh-recs"><i data-lucide="refresh-cw"></i> Recalculate</button>
                        </div>
                        <div class="card-grid" id="dashboard-recs-container">
                            ${this.renderCourseCardsHTML(d.top_recommendations)}
                        </div>
                    </div>

                    <div>
                        <div class="glass-panel" style="margin-bottom: 1.5rem;">
                            <h3><i data-lucide="bar-chart-2"></i> Priority Skill Gaps</h3>
                            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1rem;">Target: ${d.career_name}</p>
                            <div id="dashboard-gaps-list">
                                ${d.skill_gaps.length ? d.skill_gaps.map(g => `
                                    <div style="margin-bottom: 0.85rem;">
                                        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.25rem;">
                                            <span>${g.skill_name}</span>
                                            <span style="color: var(--accent-amber);">Level ${g.current_level} / ${g.required_level}</span>
                                        </div>
                                        <div class="progress-bar-bg">
                                            <div class="progress-bar-fill" style="width: ${(g.current_level / g.required_level) * 100}%"></div>
                                        </div>
                                    </div>
                                `).join('') : '<p style="font-size: 0.85rem; color: var(--text-muted);">No major skill gaps identified!</p>'}
                            </div>
                        </div>

                        <div class="glass-panel">
                            <h3><i data-lucide="activity"></i> Recent Activity</h3>
                            <div style="margin-top: 0.75rem;">
                                ${d.recent_activity.length ? d.recent_activity.map(a => `
                                    <div style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color); font-size: 0.8rem;">
                                        <div style="font-weight: 600;">${a.event_type} - ${a.course_title}</div>
                                        <div style="color: var(--text-muted); font-size: 0.72rem;">${new Date(a.created_at).toLocaleDateString()}</div>
                                    </div>
                                `).join('') : '<p style="font-size: 0.8rem; color: var(--text-muted);">No recent activity recorded.</p>'}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('btn-dashboard-refresh-recs')?.addEventListener('click', async () => {
                await this.apiFetch('/recommendations/generate/', { method: 'POST', body: JSON.stringify({ refresh: true }) });
                this.renderDashboard(container);
            });

            this.bindCourseCardEvents();
        } catch (err) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose);">Failed to load dashboard: ${err.message}</div>`;
        }
    }

    renderCourseCardsHTML(recommendations) {
        if (!recommendations || !recommendations.length) {
            return `<div class="glass-panel" style="grid-column: 1 / -1;"><p>No recommendations available. Complete your onboarding profile to generate recommendations.</p></div>`;
        }

        return recommendations.map(rec => {
            const c = rec.course;
            const exp = rec.explanation_json || {};
            const reasons = exp.reasons || [];
            const warnings = exp.warnings || [];

            return `
                <div class="course-card">
                    <div class="score-badge">${rec.final_score}% Match</div>
                    <div class="course-provider">${c.provider_name}</div>
                    <div class="course-title">${c.title}</div>
                    <div class="course-meta">
                        <span><i data-lucide="clock" style="width:14px"></i> ${c.duration_hours}h</span>
                        <span><i data-lucide="shield" style="width:14px"></i> ${c.difficulty}</span>
                        <span><i data-lucide="tag" style="width:14px"></i> ${c.cost_type}</span>
                    </div>

                    <div class="course-reasons">
                        ${reasons.slice(0, 2).map(r => `
                            <div class="reason-item"><i data-lucide="check" style="width:14px; color: var(--accent-emerald)"></i> ${r}</div>
                        `).join('')}
                        ${warnings.map(w => `
                            <div class="warning-item"><i data-lucide="alert-triangle" style="width:14px"></i> ${w}</div>
                        `).join('')}
                    </div>

                    <div class="course-actions">
                        <button class="btn btn-primary btn-sm btn-view-explanation" data-rec-id="${rec.id}">Why This?</button>
                        <a href="${c.url}" target="_blank" class="btn btn-outline btn-sm">Start Course</a>
                        <button class="icon-btn btn-bookmark-course" data-course-id="${c.id}" title="Bookmark"><i data-lucide="bookmark"></i></button>
                    </div>
                </div>
            `;
        }).join('');
    }

    bindCourseCardEvents() {
        document.querySelectorAll('.btn-view-explanation').forEach(btn => {
            btn.addEventListener('click', async () => {
                const recId = btn.getAttribute('data-rec-id');
                await this.showExplanationModal(recId);
            });
        });

        document.querySelectorAll('.btn-bookmark-course').forEach(btn => {
            btn.addEventListener('click', async () => {
                const courseId = btn.getAttribute('data-course-id');
                await this.apiFetch(`/courses/${courseId}/bookmark/`, { method: 'POST' });
                alert("Course bookmarked!");
            });
        });
    }

    async showExplanationModal(recId) {
        const modal = document.getElementById('modal-explanation');
        const body = document.getElementById('explanation-modal-body');
        if (!modal || !body) return;

        body.innerHTML = `<p><i data-lucide="loader-2" class="spin"></i> Fetching AI evidence...</p>`;
        modal.classList.remove('hidden');

        try {
            const res = await this.apiFetch(`/ai/explain-recommendation/${recId}/`);
            const d = res.data;

            body.innerHTML = `
                <div style="margin-bottom: 1rem;">
                    <span class="badge badge-emerald" style="margin-bottom: 0.5rem;">Source: ${d.source}</span>
                    <p style="font-size: 0.95rem; line-height: 1.5; color: var(--text-primary); font-weight: 500;">
                        ${d.explanation_text}
                    </p>
                </div>
                <div style="border-top: 1px solid var(--border-color); padding-top: 1rem;">
                    <h4>Evidence Breakdown</h4>
                    <ul style="margin-top: 0.5rem; padding-left: 1.2rem; font-size: 0.85rem; color: var(--text-secondary);">
                        ${d.reasons.map(r => `<li>${r}</li>`).join('')}
                    </ul>
                    ${d.warnings.length ? `
                        <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(245, 158, 11, 0.1); border-radius: var(--radius-sm);">
                            <h5 style="color: var(--accent-amber);">Prerequisite Notice</h5>
                            <ul style="font-size: 0.8rem; color: var(--accent-amber); padding-left: 1rem;">
                                ${d.warnings.map(w => `<li>${w}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
                <div style="margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 0.5rem;">
                    <button class="btn btn-outline btn-feedback-trigger" data-rec-id="${recId}">Give Feedback</button>
                </div>
            `;

            document.querySelector('.btn-feedback-trigger')?.addEventListener('click', () => {
                modal.classList.add('hidden');
                this.showFeedbackModal(recId);
            });

            if (window.lucide) lucide.createIcons();
        } catch (e) {
            body.innerHTML = `<p style="color: var(--accent-rose)">Failed to fetch explanation: ${e.message}</p>`;
        }
    }

    showFeedbackModal(recId) {
        const modal = document.getElementById('modal-feedback');
        const body = document.getElementById('feedback-modal-body');
        if (!modal || !body) return;

        body.innerHTML = `
            <form id="form-feedback">
                <div class="form-group">
                    <label class="form-label">Was this recommendation useful?</label>
                    <select class="form-control" id="feedback-helpful">
                        <option value="YES">👍 Yes, Helpful</option>
                        <option value="NO">👎 No, Not Helpful</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Reason (Optional)</label>
                    <select class="form-control" id="feedback-reason">
                        <option value="NOT_RELEVANT">Not Relevant</option>
                        <option value="TOO_EASY">Too Easy</option>
                        <option value="TOO_DIFFICULT">Too Difficult</option>
                        <option value="ALREADY_KNOW">Already Know This</option>
                        <option value="BAD_RESOURCE">Poor Course Quality</option>
                        <option value="MAYBE_LATER">Interested Later</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Rating (1 to 5 Stars)</label>
                    <input type="number" class="form-control" id="feedback-rating" min="1" max="5" value="5">
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">Submit Feedback</button>
            </form>
        `;
        modal.classList.remove('hidden');

        document.getElementById('form-feedback').addEventListener('submit', async (e) => {
            e.preventDefault();
            const helpful = document.getElementById('feedback-helpful').value;
            const reason = document.getElementById('feedback-reason').value;
            const rating = document.getElementById('feedback-rating').value;

            await this.apiFetch(`/recommendations/${recId}/feedback/`, {
                method: 'POST',
                body: JSON.stringify({ helpful, reason, rating })
            });

            modal.classList.add('hidden');
            alert("Thank you for your feedback! Your response will improve future recommendations.");
        });
    }

    /* ---------------- 2. RECOMMENDATIONS HUB VIEW ---------------- */
    async renderRecommendations(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Loading Recommendations...</p></div>`;

        try {
            const res = await this.apiFetch('/recommendations/');
            const recs = res.data;

            container.innerHTML = `
                <div class="glass-panel" style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h2>Hybrid Recommendations Engine</h2>
                            <p style="font-size: 0.85rem; color: var(--text-secondary);">Algorithm: hybrid-v1 (TF-IDF Content Similarity + Multi-factor Rule Scoring)</p>
                        </div>
                        <button class="btn btn-primary" id="btn-re-generate-recs"><i data-lucide="sparkles"></i> Refresh Engine</button>
                    </div>
                </div>

                <div class="card-grid">
                    ${this.renderCourseCardsHTML(recs)}
                </div>
            `;

            document.getElementById('btn-re-generate-recs')?.addEventListener('click', async () => {
                await this.apiFetch('/recommendations/generate/', { method: 'POST', body: JSON.stringify({ refresh: true }) });
                this.renderRecommendations(container);
            });

            this.bindCourseCardEvents();
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Error: ${e.message}</div>`;
        }
    }

    /* ---------------- 3. LEARNING ROADMAP VIEW ---------------- */
    async renderRoadmap(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Generating Learning Roadmap...</p></div>`;

        try {
            const res = await this.apiFetch('/recommendations/learning-path/');
            const d = res.data;

            if (!d.roadmap || !d.roadmap.length) {
                container.innerHTML = `<div class="glass-panel"><p>Please select a primary career goal in your student profile to view your custom roadmap.</p></div>`;
                return;
            }

            container.innerHTML = `
                <div class="glass-panel" style="margin-bottom: 1.5rem;">
                    <h2><i data-lucide="git-fork" style="color: var(--accent-cyan)"></i> Structured Learning Roadmap</h2>
                    <p style="font-size: 0.85rem; color: var(--text-secondary);">Target Career: <strong>${d.career_name}</strong></p>
                </div>

                <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                    ${d.roadmap.map(lvl => `
                        <div class="glass-panel">
                            <h3 style="margin-bottom: 1rem; color: var(--accent-blue);">${lvl.level_title}</h3>
                            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem;">
                                ${lvl.skills.map(s => `
                                    <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); padding: 0.85rem; border-radius: var(--radius-sm);">
                                        <div style="font-weight: 700; font-size: 0.95rem;">${s.skill_name}</div>
                                        <div style="font-size: 0.78rem; color: var(--text-muted);">${s.skill_category}</div>
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                                            <span class="badge ${s.status === 'COMPLETED' ? 'badge-emerald' : (s.status === 'IN_PROGRESS' ? 'badge-amber' : 'badge-blue')}">${s.status}</span>
                                            <span style="font-size: 0.8rem; font-weight: 600;">Lvl ${s.current_level}/${s.required_level}</span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Error: ${e.message}</div>`;
        }
    }

    /* ---------------- 4. SKILL GAP VIEW ---------------- */
    async renderSkillGap(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Analyzing Skill Gaps...</p></div>`;

        try {
            const res = await this.apiFetch('/students/me/skill-gaps/');
            const d = res.data;

            container.innerHTML = `
                <div class="glass-panel" style="margin-bottom: 1.5rem;">
                    <h2><i data-lucide="bar-chart-3" style="color: var(--accent-amber)"></i> Skill Gap Analysis</h2>
                    <p style="font-size: 0.85rem; color: var(--text-secondary);">Target Career: <strong>${d.career_name || 'None Selected'}</strong></p>
                </div>

                <div class="glass-panel">
                    <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                        ${d.gaps && d.gaps.length ? d.gaps.map(g => `
                            <div>
                                <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.35rem;">
                                    <span>${g.skill_name} <span class="badge badge-purple">${g.skill_category}</span></span>
                                    <span style="color: var(--accent-amber);">Current Level: ${g.current_level} / Target Level: ${g.required_level} (Gap: +${g.gap})</span>
                                </div>
                                <div class="progress-bar-bg" style="height: 12px;">
                                    <div class="progress-bar-fill" style="width: ${(g.current_level / g.required_level) * 100}%; background: linear-gradient(90deg, var(--accent-amber), var(--accent-rose));"></div>
                                </div>
                            </div>
                        `).join('') : '<p>No skill gaps identified! Your current skills fulfill the requirements of your target career.</p>'}
                    </div>
                </div>
            `;
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Error: ${e.message}</div>`;
        }
    }

    /* ---------------- 5. CAREER EXPLORER VIEW ---------------- */
    async renderCareers(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Loading Careers...</p></div>`;

        try {
            const res = await this.apiFetch('/careers/');
            const careers = res.results || res.data || res;

            container.innerHTML = `
                <div class="card-grid">
                    ${careers.map(c => `
                        <div class="glass-panel">
                            <div class="badge badge-blue" style="margin-bottom: 0.5rem;">${c.industry}</div>
                            <h3>${c.name}</h3>
                            <p style="font-size: 0.85rem; color: var(--text-secondary); margin: 0.5rem 0 1rem 0;">${c.description || 'No description'}</p>
                            <h4>Required Skills</h4>
                            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; margin-bottom: 1.25rem;">
                                ${(c.required_skills || []).map(rs => `
                                    <span class="badge badge-purple">${rs.skill.name} (Lvl ${rs.required_level})</span>
                                `).join('')}
                            </div>
                            <button class="btn btn-outline btn-select-career" data-career-id="${c.id}" style="width: 100%;">Set as Primary Goal</button>
                        </div>
                    `).join('')}
                </div>
            `;

            document.querySelectorAll('.btn-select-career').forEach(btn => {
                btn.addEventListener('click', async () => {
                    const cid = btn.getAttribute('data-career-id');
                    await this.apiFetch('/students/me/career-goals/', {
                        method: 'POST',
                        body: JSON.stringify({ career_id: parseInt(cid), is_primary: true })
                    });
                    alert("Primary career goal updated!");
                    this.renderView('dashboard');
                });
            });
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Error: ${e.message}</div>`;
        }
    }

    /* ---------------- 6. SKILL ASSESSMENTS VIEW ---------------- */
    async renderAssessments(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Loading Assessments...</p></div>`;

        try {
            const res = await this.apiFetch('/assessments/');
            const assessments = res.results || res.data || res;

            container.innerHTML = `
                <div class="card-grid">
                    ${assessments.map(a => `
                        <div class="glass-panel">
                            <div class="badge badge-emerald" style="margin-bottom: 0.5rem;">${a.skill_name}</div>
                            <h3>${a.title}</h3>
                            <p style="font-size: 0.85rem; color: var(--text-secondary); margin: 0.5rem 0 1rem 0;">${a.description}</p>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.25rem;">
                                <span><i data-lucide="clock" style="width:14px"></i> ${a.duration_minutes} mins</span> | 
                                <span>Passing: ${a.passing_score}%</span>
                            </div>
                            <button class="btn btn-primary btn-start-assessment" data-assessment-id="${a.id}" style="width: 100%;">Take Quiz</button>
                        </div>
                    `).join('')}
                </div>
            `;

            document.querySelectorAll('.btn-start-assessment').forEach(btn => {
                btn.addEventListener('click', async () => {
                    const aid = btn.getAttribute('data-assessment-id');
                    await this.startQuiz(aid, container);
                });
            });
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Error: ${e.message}</div>`;
        }
    }

    async startQuiz(assessmentId, container) {
        try {
            const res = await this.apiFetch(`/assessments/${assessmentId}/start/`, { method: 'POST' });
            const d = res.data;
            const attemptId = d.attempt_id;
            const questions = d.assessment.questions;

            let currentQIndex = 0;
            const userAnswers = {};

            const renderQuestion = () => {
                const q = questions[currentQIndex];
                container.innerHTML = `
                    <div class="wizard-card glass-panel">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                            <h3>Question ${currentQIndex + 1} of ${questions.length}</h3>
                            <span class="badge badge-amber"><i data-lucide="clock"></i> Quiz in Progress</span>
                        </div>
                        
                        <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 1.5rem;">${q.question_text}</p>

                        <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 2rem;">
                            ${q.options.map(opt => `
                                <label style="display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: var(--radius-sm); cursor: pointer;">
                                    <input type="radio" name="option" value="${opt.id}" ${userAnswers[q.id] === opt.id ? 'checked' : ''}>
                                    <span>${opt.option_text}</span>
                                </label>
                            `).join('')}
                        </div>

                        <div style="display: flex; justify-content: space-between;">
                            <button class="btn btn-outline" id="btn-quiz-prev" ${currentQIndex === 0 ? 'disabled' : ''}>Previous</button>
                            ${currentQIndex === questions.length - 1 ? `
                                <button class="btn btn-primary" id="btn-quiz-submit">Submit Quiz</button>
                            ` : `
                                <button class="btn btn-primary" id="btn-quiz-next">Next Question</button>
                            `}
                        </div>
                    </div>
                `;

                document.querySelectorAll('input[name="option"]').forEach(input => {
                    input.addEventListener('change', async (e) => {
                        const selectedOptId = parseInt(e.target.value);
                        userAnswers[q.id] = selectedOptId;
                        await this.apiFetch(`/assessment-attempts/${attemptId}/answer/`, {
                            method: 'POST',
                            body: JSON.stringify({ question_id: q.id, option_id: selectedOptId })
                        });
                    });
                });

                document.getElementById('btn-quiz-prev')?.addEventListener('click', () => {
                    if (currentQIndex > 0) { currentQIndex--; renderQuestion(); }
                });
                document.getElementById('btn-quiz-next')?.addEventListener('click', () => {
                    if (currentQIndex < questions.length - 1) { currentQIndex++; renderQuestion(); }
                });
                document.getElementById('btn-quiz-submit')?.addEventListener('click', async () => {
                    const submitRes = await this.apiFetch(`/assessment-attempts/${attemptId}/submit/`, { method: 'POST' });
                    alert(submitRes.message);
                    this.renderView('dashboard');
                });
            };

            renderQuestion();
        } catch (e) {
            alert("Error starting assessment: " + e.message);
        }
    }

    /* ---------------- 7. COURSES CATALOG VIEW ---------------- */
    async renderCourses(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Loading Course Catalog...</p></div>`;

        try {
            const res = await this.apiFetch('/courses/');
            const courses = res.results || res.data || res;

            container.innerHTML = `
                <div class="card-grid">
                    ${courses.map(c => `
                        <div class="course-card">
                            <div class="course-provider">${c.provider_name}</div>
                            <div class="course-title">${c.title}</div>
                            <div class="course-meta">
                                <span>${c.duration_hours}h</span> | 
                                <span>${c.difficulty}</span> | 
                                <span>${c.cost_type}</span>
                            </div>
                            <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1rem;">${c.description.substring(0, 120)}...</p>
                            <div class="course-actions">
                                <a href="${c.url}" target="_blank" class="btn btn-primary btn-sm" style="width: 100%;">View on Provider Site</a>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Error: ${e.message}</div>`;
        }
    }

    /* ---------------- 8. STUDENT PROFILE VIEW ---------------- */
    async renderProfile(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Loading Profile...</p></div>`;

        try {
            const res = await this.apiFetch('/students/me/');
            const p = res.data;

            container.innerHTML = `
                <div class="glass-panel wizard-card">
                    <h2>Student Academic Profile</h2>
                    <form id="form-profile" style="margin-top: 1.5rem;">
                        <div class="form-group">
                            <label class="form-label">Current Semester</label>
                            <input type="number" class="form-control" id="profile-semester" min="1" max="8" value="${p.current_semester}">
                        </div>
                        <div class="form-group">
                            <label class="form-label">CGPA</label>
                            <input type="number" step="0.1" class="form-control" id="profile-cgpa" min="0" max="10" value="${p.cgpa}">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Weekly Learning Hours</label>
                            <input type="number" class="form-control" id="profile-hours" min="1" max="50" value="${p.weekly_learning_hours}">
                        </div>
                        <button type="submit" class="btn btn-primary" style="width: 100%;">Save Changes</button>
                    </form>
                </div>
            `;

            document.getElementById('form-profile').addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.apiFetch('/students/me/', {
                    method: 'PATCH',
                    body: JSON.stringify({
                        current_semester: parseInt(document.getElementById('profile-semester').value),
                        cgpa: parseFloat(document.getElementById('profile-cgpa').value),
                        weekly_learning_hours: parseInt(document.getElementById('profile-hours').value)
                    })
                });
                alert("Profile saved!");
            });
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Error: ${e.message}</div>`;
        }
    }

    /* ---------------- 9. ONBOARDING WIZARD ---------------- */
    renderOnboarding() {
        const container = document.getElementById('view-container');
        if (!container) return;

        container.innerHTML = `
            <div class="wizard-card glass-panel">
                <h2>Student Onboarding Setup</h2>
                <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">Set up your AP college, branch, skills, and target career goal to receive custom recommendations.</p>
                <form id="form-onboarding">
                    <div class="form-group">
                        <label class="form-label">Current Semester</label>
                        <select class="form-control" id="ob-semester">
                            <option value="1">Semester 1 (1st Year)</option>
                            <option value="2">Semester 2 (1st Year)</option>
                            <option value="3">Semester 3 (2nd Year)</option>
                            <option value="4" selected>Semester 4 (2nd Year)</option>
                            <option value="5">Semester 5 (3rd Year)</option>
                            <option value="6">Semester 6 (3rd Year)</option>
                            <option value="7">Semester 7 (4th Year)</option>
                            <option value="8">Semester 8 (4th Year)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Preferred Course Difficulty</label>
                        <select class="form-control" id="ob-difficulty">
                            <option value="BEGINNER">Beginner</option>
                            <option value="INTERMEDIATE" selected>Intermediate</option>
                            <option value="ADVANCED">Advanced</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width: 100%;">Complete & Generate Recommendations</button>
                </form>
            </div>
        `;

        document.getElementById('form-onboarding').addEventListener('submit', async (e) => {
            e.preventDefault();
            const sem = parseInt(document.getElementById('ob-semester').value);
            const diff = document.getElementById('ob-difficulty').value;

            await this.apiFetch('/students/me/', {
                method: 'PATCH',
                body: JSON.stringify({ current_semester: sem, preferred_difficulty: diff, onboarding_completed: true })
            });

            await this.apiFetch('/recommendations/generate/', { method: 'POST', body: JSON.stringify({ refresh: true }) });
            this.renderView('dashboard');
        });
    }

    /* ---------------- 10. ADMIN ANALYTICS VIEW ---------------- */
    async renderAdmin(container) {
        container.innerHTML = `<div class="glass-panel"><p><i data-lucide="loader-2" class="spin"></i> Loading Admin Analytics...</p></div>`;

        try {
            const res = await this.apiFetch('/admin/dashboard/');
            const d = res.data;

            container.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon blue"><i data-lucide="users"></i></div>
                        <div class="stat-info">
                            <div class="label">Total Students</div>
                            <div class="value">${d.total_students}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon emerald"><i data-lucide="thumbs-up"></i></div>
                        <div class="stat-info">
                            <div class="label">Acceptance Rate</div>
                            <div class="value">${d.acceptance_rate}%</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon purple"><i data-lucide="book-open"></i></div>
                        <div class="stat-info">
                            <div class="label">Total Courses</div>
                            <div class="value">${d.total_courses}</div>
                        </div>
                    </div>
                </div>

                <div class="glass-panel">
                    <h3>Popular Student Careers</h3>
                    <ul style="margin-top: 1rem; padding-left: 1.2rem;">
                        ${d.popular_careers.map(pc => `<li>${pc.career__name}: ${pc.count} students</li>`).join('')}
                    </ul>
                </div>
            `;
        } catch (e) {
            container.innerHTML = `<div class="glass-panel" style="color: var(--accent-rose)">Admin access required. ${e.message}</div>`;
        }
    }

    showAuthModal(type) {
        const container = document.getElementById('view-container');
        if (!container) return;

        container.innerHTML = `
            <div class="wizard-card glass-panel">
                <h2>${type === 'login' ? 'Login to CourseAI' : 'Register Account'}</h2>
                <form id="form-auth" style="margin-top: 1.5rem;">
                    <div class="form-group">
                        <label class="form-label">Email Address</label>
                        <input type="email" class="form-control" id="auth-email" required value="student@jntua.ac.in">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" id="auth-password" required value="Student123!">
                    </div>
                    ${type === 'register' ? `
                        <div class="form-group">
                            <label class="form-label">First Name</label>
                            <input type="text" class="form-control" id="auth-first-name" required value="Rahul">
                        </div>
                    ` : ''}
                    <button type="submit" class="btn btn-primary" style="width: 100%;">${type === 'login' ? 'Login' : 'Register'}</button>
                    <p style="margin-top: 1rem; font-size: 0.85rem; text-align: center;">
                        ${type === 'login' ? 'Need an account? <a href="#" id="auth-toggle">Register here</a>' : 'Already have an account? <a href="#" id="auth-toggle">Login here</a>'}
                    </p>
                </form>
            </div>
        `;

        document.getElementById('auth-toggle')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.showAuthModal(type === 'login' ? 'register' : 'login');
        });

        document.getElementById('form-auth')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('auth-email').value;
            const password = document.getElementById('auth-password').value;

            try {
                if (type === 'login') {
                    const res = await this.apiFetch('/auth/login/', {
                        method: 'POST',
                        body: JSON.stringify({ email, password })
                    });
                    if (res.success) {
                        this.token = res.data.tokens.access;
                        localStorage.setItem('access_token', res.data.tokens.access);
                        localStorage.setItem('refresh_token', res.data.tokens.refresh);
                        localStorage.setItem('user', JSON.stringify(res.data.user));
                        this.user = res.data.user;
                        this.updateUserUI();
                        this.renderView('dashboard');
                    } else {
                        alert(res.message);
                    }
                } else {
                    const firstName = document.getElementById('auth-first-name').value;
                    const res = await this.apiFetch('/auth/register/', {
                        method: 'POST',
                        body: JSON.stringify({ email, password, confirm_password: password, first_name: firstName, role: 'student' })
                    });
                    if (res.success) {
                        this.token = res.data.tokens.access;
                        localStorage.setItem('access_token', res.data.tokens.access);
                        localStorage.setItem('user', JSON.stringify(res.data.user));
                        this.user = res.data.user;
                        this.updateUserUI();
                        this.renderOnboarding();
                    } else {
                        alert(res.message);
                    }
                }
            } catch (err) {
                alert("Auth error: " + err.message);
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new CourseAIApp();
});
