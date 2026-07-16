| Issue                | Severity | Business Impact           | Cleaning Strategy            |
| -------------------- | -------- | ------------------------- | ---------------------------- |
| Duplicate rows       | High     | Double-counted sales      | Remove duplicates            |
| Product names        | High     | Incorrect reporting       | Standardize names            |
| Branch names         | High     | Incorrect branch KPIs     | Standardize names            |
| Date formats         | High     | Parsing failures          | Convert to datetime          |
| Price stored as text | High     | Arithmetic errors         | Convert to numeric           |
| Missing customer     | Low      | Limited customer analysis | Leave blank or label Unknown |
| Negative quantity    | High     | Invalid sales             | Investigate or remove        |
| Quantity = 100       | Medium   | Possible outlier          | Validate before removing     |
