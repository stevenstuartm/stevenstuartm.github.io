/**
 * Reading Progress Tracker
 * Tracks user's reading position in study guides using localStorage
 */

class ReadingProgressTracker {
    constructor() {
        this.storageKey = 'studyGuideProgress';
        this.maxHistoryItems = 10;
        this.saveDebounceMs = 5000; // Save every 5 seconds while scrolling
        this.minGuideHeight = 1000; // Don't track guides shorter than this
        this.completeThreshold = 0.95; // Mark as complete at 95% scroll

        this.saveTimeout = null;
        this.isTracking = false;
    }

    /**
     * Initialize tracking for the current guide page
     * @param {Object} guideData - { url, title, category }
     */
    initTracking(guideData) {
        if (!this.shouldTrack()) {
            return;
        }

        this.currentGuide = guideData;
        this.isTracking = true;

        // Check if returning to a guide with saved progress
        this.checkForSavedProgress();

        // Set up scroll tracking
        window.addEventListener('scroll', () => this.onScroll());
        window.addEventListener('beforeunload', () => this.saveProgress(true));

        // Save initial position
        this.saveProgress();
    }

    /**
     * Check if we should track this guide
     */
    shouldTrack() {
        const prefs = this.getPreferences();
        if (!prefs.trackProgress) {
            return false;
        }

        // Don't track if guide is too short
        const pageHeight = document.documentElement.scrollHeight - window.innerHeight;
        return pageHeight >= this.minGuideHeight;
    }

    /**
     * Check if user is returning to a guide with saved progress
     */
    checkForSavedProgress() {
        const data = this.getData();
        if (!data.currentGuide) {
            return;
        }

        const current = data.currentGuide;
        if (current.url === this.currentGuide.url && current.scrollPosition > 100) {
            // Show prompt to resume
            this.showResumePrompt(current);
        }
    }

    /**
     * Show prompt to resume reading from saved position
     */
    showResumePrompt(savedGuide) {
        // Only show if not already at that position
        if (window.scrollY > 50) {
            return;
        }

        const banner = document.createElement('div');
        banner.className = 'resume-reading-prompt';
        banner.innerHTML = `
            <div class="resume-reading-content">
                <span class="resume-reading-text">
                    📖 Resume reading from ${savedGuide.scrollPercent}%?
                </span>
                <div class="resume-reading-actions">
                    <button class="resume-btn" id="resumeReadingBtn">Resume</button>
                    <button class="dismiss-btn" id="dismissResumeBtn">Start from top</button>
                </div>
            </div>
        `;

        document.body.insertBefore(banner, document.body.firstChild);

        // Handle resume button
        document.getElementById('resumeReadingBtn').addEventListener('click', () => {
            window.scrollTo({
                top: savedGuide.scrollPosition,
                behavior: 'smooth'
            });
            banner.remove();
        });

        // Handle dismiss button
        document.getElementById('dismissResumeBtn').addEventListener('click', () => {
            banner.remove();
        });
    }

    /**
     * Handle scroll events
     */
    onScroll() {
        if (!this.isTracking) {
            return;
        }

        // Debounce saves
        clearTimeout(this.saveTimeout);
        this.saveTimeout = setTimeout(() => {
            this.saveProgress();
        }, this.saveDebounceMs);
    }

    /**
     * Save current reading progress
     */
    saveProgress(immediate = false) {
        if (!this.isTracking) {
            return;
        }

        const scrollPosition = window.scrollY;
        const pageHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = Math.round((scrollPosition / pageHeight) * 100);

        const progressData = {
            url: this.currentGuide.url,
            title: this.currentGuide.title,
            category: this.currentGuide.category,
            scrollPosition: scrollPosition,
            scrollPercent: Math.min(scrollPercent, 100),
            lastRead: new Date().toISOString()
        };

        const data = this.getData();

        // Check if guide is completed
        if (scrollPercent >= this.completeThreshold * 100) {
            this.markAsComplete(progressData);
            data.currentGuide = null; // Clear current since it's complete
        } else {
            data.currentGuide = progressData;
        }

        this.setData(data);
    }

    /**
     * Mark guide as completed and add to history
     */
    markAsComplete(guideData) {
        const data = this.getData();

        // Add to history
        const historyItem = {
            url: guideData.url,
            title: guideData.title,
            category: guideData.category,
            scrollPercent: 100,
            completedAt: new Date().toISOString()
        };

        // Remove any existing entry for this guide
        data.readingHistory = data.readingHistory.filter(item => item.url !== guideData.url);

        // Add to beginning and limit history size
        data.readingHistory.unshift(historyItem);
        data.readingHistory = data.readingHistory.slice(0, this.maxHistoryItems);

        this.setData(data);
    }

    /**
     * Get all progress data from localStorage
     */
    getData() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (!stored) {
                return this.getDefaultData();
            }
            return JSON.parse(stored);
        } catch (e) {
            console.error('Error reading progress data:', e);
            return this.getDefaultData();
        }
    }

    /**
     * Save progress data to localStorage
     */
    setData(data) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(data));
        } catch (e) {
            console.error('Error saving progress data:', e);
        }
    }

    /**
     * Get default data structure
     */
    getDefaultData() {
        return {
            currentGuide: null,
            readingHistory: [],
            preferences: {
                trackProgress: true
            }
        };
    }

    /**
     * Get user preferences
     */
    getPreferences() {
        const data = this.getData();
        return data.preferences || {
            trackProgress: true
        };
    }

    /**
     * Update user preferences
     */
    setPreferences(prefs) {
        const data = this.getData();
        data.preferences = { ...data.preferences, ...prefs };
        this.setData(data);
    }

    /**
     * Get current reading progress (for use in homepage)
     */
    getCurrentProgress() {
        const data = this.getData();
        return data.currentGuide;
    }

    /**
     * Get reading history
     */
    getHistory() {
        const data = this.getData();
        return data.readingHistory || [];
    }

    /**
     * Clear all progress data
     */
    clearAll() {
        localStorage.removeItem(this.storageKey);
    }

    /**
     * Format time ago string
     */
    static formatTimeAgo(isoString) {
        const date = new Date(isoString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffMins < 1) return 'just now';
        if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
        if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

        return date.toLocaleDateString();
    }
}

// Create global instance
window.ReadingProgressTracker = ReadingProgressTracker;
