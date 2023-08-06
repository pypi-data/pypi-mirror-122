# House prediction web app
----------------------------

This project intention to Predict different House type Prices in different states in AUS. This Model helps to Real estates to quickly predict house prices in AUS.

 ![reusable-Naga--Ml--Model--Apps-orange (1)](https://user-images.githubusercontent.com/92179722/136643724-61649ee7-76b5-4027-8066-eef510fd5d63.png)  ![status-stable-yellowgreen](https://user-images.githubusercontent.com/92179722/136643760-a592249d-5d9c-40d9-a5fe-a9a34898a988.png)  ![pypi-v0 0 (2)](https://user-images.githubusercontent.com/92179722/136643761-da4fbe5d-623e-4bcb-85d8-5949aad11a9f.png)  ![licience-MIT-green](https://user-images.githubusercontent.com/92179722/136643779-24feba85-bba1-4fdc-92ca-02b0013b6af0.png)

## Quick start


1. Add ``Deployment,widget_tweaks,crispy_forms`` to your INSTALLED_APPS setting like this::
    
    INSTALLED_APPS = [
    
     			'Deployment',
                       'widget_tweaks',
                       'crispy_forms',  
   	            ]
    

2. Include the every app URLconf in your project urls.py like this
   ``` bash
	urlpatterns = [
			path('admin/', admin.site.urls),
			path('',include('Deployment.urls')),
		      ]
    ```

3. Run ``python manage.py migrate`` to create the ``Deployment``  models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a those three apps (you'll need the Admin app enabled).
   - create a admin 
   	-- python manage.py createsuperuser

5. Visit http://127.0.0.1:8000/ for homepage
6. Detail documentation [click here](https://github.com/Nagababu91768/house-price-prediction-ml-app/blob/master/README.md)

## License
[MIT](https://choosealicense.com/licenses/mit/)