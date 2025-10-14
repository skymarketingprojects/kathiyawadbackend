# app/views.py

from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpRequest

from .Utils.response import serverResponse
from .controller.controller import AppController
from kathiyawadApi.Utils.code import ResponseCode
from kathiyawadApi.Utils.message import ResponseMessage
from kathiyawadApi.Utils.status import ResponseStatus

# Instantiate the controller class
appController = AppController()

# --- Product Views ---

@api_view(['GET'])
def productsListView(request: HttpRequest):
    try:
        if 'querys' in request.GET:
            response = appController.SearchProducts(request)
        else:
            response = appController.GetProducts(request)
            
        return serverResponse(
            status=response.status,
            code=response.code,
            data=response.data,
            message=response.message
        )
    except Exception as e:
        return serverResponse(
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.PRODUCTS_FETCHED_ERROR
            )

@api_view(['GET'])
def productDetailView(request: HttpRequest, productId: int):
    try:
        response = appController.GetProductById(productId)
        
        return serverResponse(
            status=response.status,
            code=response.code,
            data=response.data,
            message=response.message
        )
    except Exception as e:
        return serverResponse(
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.PRODUCT_FETCHED_ERROR
            )

# --- Blog Views ---

@api_view(['GET'])
def blogsListView(request: HttpRequest):
    try:
        response = appController.GetBlogs(request)
        
        return serverResponse(
            status=response.status,
            code=response.code,
            data=response.data,
            message=response.message
        )
    except Exception as e:
        return serverResponse(
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.BLOGS_FETCHED_ERROR
            )

@api_view(['GET'])
def blogsSearchByCategoryView(request: HttpRequest, categoryId: int):
    try:
        response = appController.FilterBlogsByCategory(categoryId, request)
        
        return serverResponse(
            status=response.status,
            code=response.code,
            data=response.data,
            message=response.message
        )
    except Exception as e:
        return serverResponse(
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.BLOGS_FETCHED_ERROR
            )

@api_view(['GET'])
def blogDetailView(request: HttpRequest, blogId: int):
    try:
        response = appController.GetBlogById(blogId)
        
        return serverResponse(
            status=response.status,
            code=response.code,
            data=response.data,
            message=response.message
        )
    except Exception as e:
        return serverResponse(
            status=ResponseStatus.ERROR,
            code=ResponseCode.ERROR,
            data={"error": str(e)},
            message=ResponseMessage.BLOG_FETCHED_ERROR
            )