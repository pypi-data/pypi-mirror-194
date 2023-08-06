# Github Scrape

This version scrapes github page for a specified user 
displays a report on the user 

The report contains:
- [x] Number of followers
- [x] Number of users being followed
- [x] Nmber of people following but not following back 
- [x] Opposite of '3.'
- [x] Check number of repositories
- [x] List repositories

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
