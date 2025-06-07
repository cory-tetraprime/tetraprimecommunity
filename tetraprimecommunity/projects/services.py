from .models import TeamMemberNote, NextAction


class Planner:
    def __init__(self, project):
        self.project = project

    def add_member_note(self, membership, title, content):
        """Add a note for a specific project membership."""
        return TeamMemberNote.objects.create(
            project_membership=membership,
            title=title,
            content=content
        )

    def get_member_notes(self, membership):
        """Retrieve all notes for a specific project membership."""
        return membership.notes.all()

    def delete_note(self, note_id):
        """Delete a specific note by its ID."""
        try:
            note = TeamMemberNote.objects.get(id=note_id)
            note.delete()
            return True
        except TeamMemberNote.DoesNotExist:
            return False

    def create_action(self, title, action_stage, due_date=None, assigned_to=None, notes=''):
        """Create a new action for the project."""
        return NextAction.objects.create(
            project=self.project,
            title=title,
            action_stage=action_stage,
            due_date=due_date,
            assigned_to=assigned_to,
            notes=notes
        )

    def get_project_actions(self):
        """Retrieve all actions for the project."""
        return self.project.actions.all()

    def get_member_actions(self, membership):
        """Retrieve all actions assigned to a specific project membership."""
        return membership.actions.all()

    def delete_action(self, action_id):
        """Delete a specific action by its ID."""
        try:
            action = NextAction.objects.get(id=action_id)
            action.delete()
            return True
        except NextAction.DoesNotExist:
            return False