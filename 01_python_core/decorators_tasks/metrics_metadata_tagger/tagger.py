import functools

def tag_metric_metadata(**metadata):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        for key, value in metadata.items():
            setattr(wrapper, key, value)
            
        return wrapper
    return decorator

@tag_metric_metadata(
    owner="product_growth_team", 
    data_source="clickhouse_events", 
    is_critical=True,
    sla_minutes=15
)
def calculate_retention_rate(cohort_id, day):
    if not cohort_id:
        raise ValueError("cohort_id не может быть пустым")
    return 25.5

if __name__ == "__main__":
    retention = calculate_retention_rate(cohort_id="2023-10-W1", day=7)
    print(retention)
    print(calculate_retention_rate.owner)