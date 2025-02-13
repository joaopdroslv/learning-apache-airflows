## List of available Airflow trigger rules

**The following trigger rules are available:**

| **rule** | **what is does** |
| ---- | ------------ |
| `all_success (default)` | The task runs only when all upstream tasks have succeeded. |
| `all_failed` | The task runs only when all upstream tasks are in a failed or upstream_failed state. |
| `all_done` | The task runs once all upstream tasks are done with their execution. |
| `all_skipped` | The task runs only when all upstream tasks have been skipped. |
| `one_failed` | The task runs when at least one upstream task has failed. |
| `one_success` | The task runs when at least one upstream task has succeeded. |
| `one_done` | The task runs when at least one upstream task has either succeeded or failed. |
| `none_failed `| The task runs only when all upstream tasks have succeeded or been skipped. |
| `none_failed_min_one_success` | The task runs only when all upstream tasks have not failed or upstream_failed, and at least one upstream task has succeeded. | 
| `none_skipped` | The task runs only when no upstream task is in a skipped state. |
| `always` | The task runs at any time. |