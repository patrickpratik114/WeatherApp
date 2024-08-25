from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        try:
            res = urllib.request.urlopen(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=eb152b04e9dba5ee0b82893d9ad4a7cc').read()
            json_data = json.loads(res)
            
            # Converting temperature from Kelvin to Celsius
            temp_kelvin = float(json_data['main']['temp'])
            temp_celsius = round(temp_kelvin - 273.15, 2)
            
            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": f"{json_data['coord']['lon']} {json_data['coord']['lat']}",
                "temp": f"{temp_celsius}C",
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
            }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                data = {"error": "Invalid Input"}
            else:
                data = {"error": f"An error occurred: {str(e)}"}
        except Exception as e:
            data = {"error": f"An error occurred: {str(e)}"}
    return render(request, 'index.html', {'city': city, "data":data})