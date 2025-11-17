from app.models import Topic, Subject

def subject_progress(subject: Subject) -> float:
    """Return percent (0-100) of completed topics for a subject."""
    topics = subject.topics.order_by(Topic.order.asc()).all()
    total = len(topics)
    if not total:
        return 0.0
    completed = sum(1 for t in topics if t.is_completed)
    return round(completed / total * 100, 1)

def topics_progress(topics) -> float:
    """Return progress percent for an iterable of Topic objects."""
    topics_list = list(topics)
    total = len(topics_list)
    if not total:
        return 0.0
    completed = sum(1 for t in topics_list if t.is_completed)
    return round(completed / total * 100, 1)