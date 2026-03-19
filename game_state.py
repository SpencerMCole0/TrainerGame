import time

class GameState:
    def __init__(self, player):
        self.player = player
        self.last_rep_time = 0

    def _current_day(self):
        return time.localtime().tm_yday

    def _reset_daily_budget(self):
        self.player.best_daily_gymcoins = max(self.player.best_daily_gymcoins, self.player.daily_gymcoins_earned)
        self.player.daily_gymcoins_earned = 0.0
        self.player.active_seconds_remaining = self.player.daily_active_budget
        self.player.daily_sessions_used = 0
        self.player.current_session_seconds_remaining = 0.0

    def can_rep(self):
        # Requires cooldown and remaining active session seconds.
        if time.time() - self.last_rep_time < self.player.get_current_rest_time():
            return False
        if self.player.active_seconds_remaining < 0.5:
            return False

        # If in an active session, allow reps.
        if self.player.current_session_seconds_remaining >= 0.5:
            return True

        # If session ended, allow a new one only if daily sessions remain.
        return self.player.daily_sessions_used < 2

    def perform_rep(self):
        # Update daily budget based on date
        today = self._current_day()
        if today != self.player._active_day:
            self.player._active_day = today
            self._reset_daily_budget()

        if not self.can_rep():
            if self.player.active_seconds_remaining < 0.5 or self.player.daily_sessions_used >= 2:
                return "🛌 Active sessions finished for today. Come back tomorrow!"
            return "⏳ Resting..."

        # Start a new session if needed
        if self.player.current_session_seconds_remaining < 0.5:
            self.player.daily_sessions_used += 1
            self.player.current_session_seconds_remaining = 10 * 60  # 10 minute session

        now = time.time()
        if self.last_rep_time > 0:
            delta = now - self.last_rep_time
            if delta > 0:
                rep_sec = 1.0 / delta
                if rep_sec > self.player.best_rep_per_sec:
                    self.player.best_rep_per_sec = rep_sec

        self.last_rep_time = now
        self.player.active_seconds_remaining = max(0.0, self.player.active_seconds_remaining - 0.5)
        self.player.current_session_seconds_remaining = max(0.0, self.player.current_session_seconds_remaining - 0.5)
        self.player.reps += 1
        earned = self.player.earn_gym_coins()

        msg = f"🏋️‍♂️ Rep done! Earned {earned:.2f} GymCoins."
        if self.player.current_session_seconds_remaining == 0.0:
            msg += " Session complete!"
        return msg

    def update(self, dt):
        # Daily reset for active session budget
        today = self._current_day()
        if today != self.player._active_day:
            self.player._active_day = today
            self._reset_daily_budget()

        # Passive income from trainers
        if self.player.trainer_level > 0:
            passive_reps = self.player.get_passive_reps_per_second() * dt
            if passive_reps > 0:
                self.player.reps += passive_reps
                self.player.earn_gym_coins(reps=passive_reps)
