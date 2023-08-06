# Github Scrape

This version scrapes github page for a specified user 
displays a report on the user 

The report contains:
1. Number of followers
2. Number of users being followed
3. Nmber of people following but not following back 
4. Opposite of '3.'
5. Check number of repositories

## Usage

To use the package, you have to import using:
`from akinyeleib import work`

The function needed in the package is 
`work.check()`

You can as well as use alias:
`from akinyeleib import work as ib`
`ib.check()`

The check() which returns a dictionary object
`result = ib.check()`

We can then perform a runtime check on the object:
`print(type(result))`

### Thank you.