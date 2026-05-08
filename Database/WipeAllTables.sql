TRUNCATE TABLE
  public.comments,
  public.task_labels,
  public.task_assignments,
  public.tasks,
  public.sprints,
  public.employee_skills,
  public.project_members,
  public.components,
  public.labels,
  public.projects,
  public.employees
RESTART IDENTITY CASCADE;