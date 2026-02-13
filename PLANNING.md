# Problem Statement
We'd like to be able to import an arbitrary CSV file into GEMS GDA for analysis. DLOG99 will convert a CSV into an STF but the input CSV must be structured in a certain way. This solution will facilitate the conversion of an arbitrary CSV format into the DLOG99-compatible format.

# Requirements
- Solution shall compute total time if necessary.
- Solution shall relocate total time to the first column if necessary.
- Solution shall convert latitude and longitude from degrees to radians if necessary.
- Solution shall have predefined CSV import templates for common file structurings.

# Issues
- In CSV2GEMS.py, we ran into an issue. We store the name of the /initial/ time column, but we don't store the name of the /final/ time column. If shouldConvertTimeColumn is true, we will end up creating a new time column. This comes into play when we want to rearrange the order of the columns. We want the /final/ time column to be first, but we don't know the name of the final time column. I'll need to figure out a way to solve this.