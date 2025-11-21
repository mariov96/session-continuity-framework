import json
import time
from datetime import datetime

class SCFAnalytics:
    """
    Handles tracking, calculating, and reporting of SCF productivity metrics.
    """
    def __init__(self, buildstate_path):
        """
        Initializes the analytics system with the path to the project's buildstate.json.

        Args:
            buildstate_path (str): The full path to the buildstate.json file.
        """
        self.buildstate_path = buildstate_path
        self.data = self._load_analytics_data()

    def _load_analytics_data(self):
        """
        Loads the 'scf_analytics' section from the buildstate.json file.
        Initializes it with default values if it doesn't exist.
        """
        try:
            with open(self.buildstate_path, 'r') as f:
                buildstate = json.load(f)
            
            if 'scf_analytics' not in buildstate:
                buildstate['scf_analytics'] = self._get_default_schema()
                # Immediately save the buildstate to include the new analytics section
                self._save_buildstate(buildstate)

            return buildstate.get('scf_analytics', self._get_default_schema())
        except (FileNotFoundError, json.JSONDecodeError):
            # If the buildstate doesn't exist or is invalid, start with a default schema
            return self._get_default_schema()

    def _save_analytics_data(self):
        """
        Saves the current analytics data back to the buildstate.json file.
        """
        try:
            with open(self.buildstate_path, 'r') as f:
                buildstate = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file is gone or corrupted, we can't save.
            # A more robust system might log this error.
            print(f"Warning: Could not read {self.buildstate_path}. Analytics data not saved.")
            return

        buildstate['scf_analytics'] = self.data
        self._save_buildstate(buildstate)

    def _save_buildstate(self, buildstate_data):
        """Helper to save the full buildstate dictionary to file."""
        with open(self.buildstate_path, 'w') as f:
            json.dump(buildstate_data, f, indent=4)

    def _get_default_schema(self):
        """Returns the default structure for the scf_analytics data."""
        return {
            "metadata": {
                "since": datetime.utcnow().isoformat(),
                "version": "1.0"
            },
            "sessions": {
                "session_count": 0,
                "total_time_saved_minutes": 0,
                "context_reuse_count": 0,
                "avg_session_quality": 0.0
            },
            "learning": {
                "patterns_learned": 0,
                "patterns_applied": 0
            },
            "velocity": {
                "decisions_tracked": 0,
                "features_completed": 0
            }
        }

    def start_session(self):
        """Marks the start of a new session for timing purposes."""
        self.session_start_time = time.time()
        self.data['sessions']['session_count'] += 1
        print("SCF Analytics: Session started.")

    def end_session(self, time_saved_minutes=0, context_reused=False, quality_rating=None):
        """
        Marks the end of a session and records the metrics.

        Args:
            time_saved_minutes (int): Estimated minutes saved in this session by using SCF.
            context_reused (bool): Whether buildstate context was successfully reused.
            quality_rating (float): A rating for the session's effectiveness (e.g., 1-5).
        """
        if not hasattr(self, 'session_start_time'):
            print("Warning: end_session() called without start_session(). Cannot record metrics.")
            return

        session_duration = (time.time() - self.session_start_time) / 60
        print(f"SCF Analytics: Session ended. Duration: {session_duration:.2f} minutes.")

        self.data['sessions']['total_time_saved_minutes'] += time_saved_minutes
        if context_reused:
            self.data['sessions']['context_reuse_count'] += 1

        if quality_rating is not None:
            total_sessions = self.data['sessions']['session_count']
            current_avg = self.data['sessions']['avg_session_quality']
            # Update the moving average for session quality
            self.data['sessions']['avg_session_quality'] = ((current_avg * (total_sessions - 1)) + quality_rating) / total_sessions

        self._save_analytics_data()
        print("SCF Analytics: Session data saved.")

    def track_event(self, event_type, count=1):
        """
        Tracks a specific event, like a decision made or a feature completed.

        Args:
            event_type (str): The name of the metric to update (e.g., 'patterns_learned').
            count (int): The number to increment the metric by.
        """
        # Find the correct category for the event
        for category in ['learning', 'velocity']:
            if event_type in self.data[category]:
                self.data[category][event_type] += count
                self._save_analytics_data()
                print(f"SCF Analytics: Tracked event '{event_type}', new total: {self.data[category][event_type]}.")
                return
        
        print(f"Warning: Analytics event type '{event_type}' not found in schema.")

    def get_report(self):
        """
        Generates a human-readable report of the current analytics.
        """
        report = f"""
        ## SCF Analytics Report
        -------------------------
        - Tracking Since: {self.data['metadata']['since']}
        
        ### Session Performance
        - Total Sessions: {self.data['sessions']['session_count']}
        - Total Time Saved: {self.data['sessions']['total_time_saved_minutes']} minutes
        - Context Reuses: {self.data['sessions']['context_reuse_count']}
        - Average Session Quality: {self.data['sessions']['avg_session_quality']:.2f}

        ### Project Velocity
        - Decisions Tracked: {self.data['velocity']['decisions_tracked']}
        - Features Completed: {self.data['velocity']['features_completed']}

        ### Cross-Project Learning
        - Patterns Learned: {self.data['learning']['patterns_learned']}
        - Patterns Applied: {self.data['learning']['patterns_applied']}
        -------------------------
        """
        return report

if __name__ == '__main__':
    # Example Usage (for direct testing of this script)
    # This requires a dummy buildstate.json in the same directory
    print("Running SCFAnalytics direct test...")
    dummy_buildstate_path = './buildstate.json'
    
    # Create a dummy buildstate if it doesn't exist
    try:
        with open(dummy_buildstate_path, 'r') as f:
            pass
    except FileNotFoundError:
        with open(dummy_buildstate_path, 'w') as f:
            json.dump({"project_name": "Analytics Test"}, f, indent=4)

    analytics = SCFAnalytics(dummy_buildstate_path)
    
    analytics.start_session()
    time.sleep(0.1) # Simulate work
    analytics.end_session(time_saved_minutes=15, context_reused=True, quality_rating=4.5)

    analytics.track_event('decisions_tracked', count=5)
    analytics.track_event('features_completed')
    analytics.track_event('patterns_learned')
    analytics.track_event('patterns_applied')

    print(analytics.get_report())

    # Clean up the dummy file
    import os
    os.remove(dummy_buildstate_path)
    print("Direct test finished and dummy buildstate.json removed.")