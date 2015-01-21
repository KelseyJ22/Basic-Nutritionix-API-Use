import web
import requests

render = web.template.render('templates/')

urls = (
  '/', 'index',
  '/search', 'search'
  )

def parse(json):
  res = json['results'] # get inside the first level
  result_string = '<b> <i> You searched for \"' + res[0]['parsed_query']['query'] + '\" </b> </i> <br>'
  result_string += 'Serving size: ' + str(res[0]['serving_qty']) + res[0]['serving_unit'] + ' <br> <br>'
  result_string += '<b> Nutrient profile: </b><br>'
  for nutrient in res[0]['nutrients']:
    if nutrient['value'] != 0: # don't display the nutrients that aren't present in this food
      result_string += str(nutrient['value']) + nutrient['unit'] + ' ' + nutrient['name'] + ' <br>'
  return result_string

class search:
  def GET(self):
        results = 'Please enter a food to search.'
        return render.search(results)

  def POST(self):
    params = web.input()
    header = {'X-APP-ID': '797ba6a3', 'X-APP-KEY': '5cec736db3c993907641d9350127eafb', 'Content-Type':'text/plain'} # request body
    form_input = web.input(name="search_form")
    r = requests.request('POST', "https://apibeta.nutritionix.com/v2/natural", data = form_input['search'], headers = header)
    if r.status_code < 400: # no error
      results = parse(r.json()) # response json
      return render.search(results = results)
    else:
      results = 'Error performing search. Please try again.'
      return render.search(results)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()