from ..models import AuditEvent


def append_audit_event(actor_id, action, description, subject_type=None, subject_id=None):
    event = AuditEvent(
        actor_id=actor_id,
        action=action,
        description=description,
        subject_type=subject_type,
        subject_id=subject_id,
    )
    return event
