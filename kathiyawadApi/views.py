# app/views.py

from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpRequest

from .Utils.response import serverResponse
from .controller.controller import AppController
from .controller.HeroController.HeroController import HeroController
from kathiyawadApi.Utils.code import ResponseCode
from kathiyawadApi.Utils.message import ResponseMessage
from kathiyawadApi.Utils.status import ResponseStatus

# Instantiate the controller class
appController = AppController()

# --- Product Views ---

@api_view(['GET'])
def productsListView(request: HttpRequest):
    productResponse = None
    try:
        if 'querys' in request.GET:
            productResponse = appController.SearchProducts(request)
        else:
            productResponse = appController.GetProducts(request)
            
        return serverResponse(
            response=productResponse.response,
            status=productResponse.status,
            code=productResponse.code,
            data=productResponse.data,
            message=productResponse.message
        )
    except Exception as e:
        return serverResponse(
            response=False,
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.PRODUCTS_FETCHED_ERROR
            )

@api_view(['GET'])
def productForHomeView(request: HttpRequest):
    try:
        productResponse = appController.GetProductForHome()
        
        return serverResponse(
            response=productResponse.response,
            status=productResponse.status,
            code=productResponse.code,
            data=productResponse.data,
            message=productResponse.message
        )
    except Exception as e:
        return serverResponse(
            response=False,
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.PRODUCTS_FETCHED_ERROR
            )
@api_view(['GET'])
def productDetailView(request: HttpRequest, productId: int):
    try:
        productResponse = appController.GetProductById(productId)
        
        return serverResponse(
            response=productResponse.response,
            status=productResponse.status,
            code=productResponse.code,
            data=productResponse.data,
            message=productResponse.message
        )
    except Exception as e:
        return serverResponse(
            response=False,
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.PRODUCT_FETCHED_ERROR
            )

# --- Blog Views ---

@api_view(['GET'])
def blogsListView(request: HttpRequest):
    try:
        blogResponse = appController.GetBlogs(request)
        
        return serverResponse(
            response=blogResponse.response,
            status=blogResponse.status,
            code=blogResponse.code,
            data=blogResponse.data,
            message=blogResponse.message
        )
    except Exception as e:
        return serverResponse(
            response=False,
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.BLOGS_FETCHED_ERROR
            )

@api_view(['GET'])
def blogsSearchByCategoryView(request: HttpRequest, categoryId: int):
    try:
        blogResponse = appController.FilterBlogsByCategory(categoryId, request)
        
        return serverResponse(
            response=blogResponse.response,
            status=blogResponse.status,
            code=blogResponse.code,
            data=blogResponse.data,
            message=blogResponse.message
        )
    except Exception as e:
        return serverResponse(
            response=False,
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.BLOGS_FETCHED_ERROR
            )

@api_view(['GET'])
def blogDetailView(request: HttpRequest, blogId: int):
    try:
        blogResponse = appController.GetBlogById(blogId)
        
        return serverResponse(
            response=blogResponse.response,
            status=blogResponse.status,
            code=blogResponse.code,
            data=blogResponse.data,
            message=blogResponse.message
        )
    except Exception as e:
        return serverResponse(
            response=False,
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.BLOG_FETCHED_ERROR
            )
    
# --- Hero Views ---

@api_view(['GET'])
def heroImagesView(request: HttpRequest):
    try:
        heroresponse = HeroController.GetImageByPage(request)
        
        return serverResponse(
            response=heroresponse.response,
            status=heroresponse.status,
            code=heroresponse.code,
            data=heroresponse.data,
            message=heroresponse.message
        )
    except Exception as e:
        return serverResponse(
            response=False,
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.HERO_IMAGES_FETCHED_ERROR
            )