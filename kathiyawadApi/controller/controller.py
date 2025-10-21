# app/controller/controller.py

from kathiyawadApi.models import Product, ProductCategory, DietryNeeds, Blog, BlogCategory
from kathiyawadApi.Utils.response import localResponse
from kathiyawadApi.Utils.helpers import paginateData, createWhatsappLink
from django.db.models import Q 
from kathiyawadApi.Utils.code import ResponseCode
from kathiyawadApi.Utils.message import ResponseMessage
from kathiyawadApi.Utils.status import ResponseStatus
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
class AppController:
    """Contains all the main business logic functions."""
    
    # --- Shared Serialization Logic (Simulating DRF Output) ---
    def _SerializeProductList(self, queryset):
        """Serializes minimal data for list views."""
        serializedData = []
        for product in queryset:
            serializedData.append({
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "imageUrl": product.image.url, 
                "description": product.metaDescription,
            })
        return serializedData

    def _SerializeProductDetail(self, product):
        """Serializes full data for detail view."""
        return {
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "imageUrl": product.image.url,
            "metaDescription": product.metaDescription,
            "description": product.description.html, 
            "ingredients": product.ingredients.html,
            "shippingAndDelivery": product.shippingAndDelivery.html,
            "categories": [c.label for c in product.category.all()],
            "dietryNeeds": [d.label for d in product.dietryNeeds.all()],
            "whatsappLink": createWhatsappLink(product.title), 
            "relatedProducts": [{"id": p.id, "title": p.title} for p in product.relatedProducts.all()]
        }
        
    def _SerializeBlogList(self, queryset):
        """Serializes minimal data for blog list views."""
        serializedData = []
        for blog in queryset:
            serializedData.append({
                "id": blog.id,
                "title": blog.title,
                "description": blog.description,
                "thumbnailUrl": blog.thumbnail.url,
            })
        return serializedData
        
    def _SerializeBlogDetail(self, blog):
        """Serializes full data for blog detail view."""
        return {
            "id": blog.id,
            "title": blog.title,
            "description": blog.description,
            "thumbnailUrl": blog.thumbnail.url,
            "imageUrl": blog.image.url,
            # QuillField content is returned as a string (HTML/Delta)
            "content": blog.content.html, 
            "categories": [c.label for c in blog.category.all()],
        }

    # --- Product Functions ---

    def GetProducts(self, request:HttpRequest):
        try:
            allProducts = Product.objects.all().order_by('-id')

            # --- Pagination ---
            page = request.GET.get('page', 1)
            pageSize = request.GET.get('pageSize', 6)

            paginator = Paginator(allProducts, pageSize)

            products_page = paginator.page(page)
            print(f"products_page: {products_page.object_list}")

            serializedData = self._SerializeProductList(products_page.object_list)
            print(f"serializedData: {serializedData}")

            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data={
                    "items": serializedData,
                    
                        "totalItems": paginator.count,
                        "totalPages": paginator.num_pages,
                        "currentPage": products_page.number,
                        "hasNext": products_page.has_next(),
                        "hasPrevious": products_page.has_previous(),
                    
                },
                message=ResponseMessage.PRODUCTS_FETCHED_SUCCESS
            )
        except Exception as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.PRODUCTS_FETCHED_ERROR
            )

    def GetProductForHome(self):
        try:
            productCat = ProductCategory.objects.all()
            productsData = []
            productsList = []
            for cat in productCat:
                product = Product.objects.filter(category=cat).order_by('-id').first()
                productsList.append(product)
            productsData = self._SerializeProductList(productsList)
            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data=productsData,
                message=ResponseMessage.PRODUCTS_FETCHED_SUCCESS
                )
        except Exception as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.PRODUCTS_FETCHED_ERROR
                )
    def GetProductById(self, productId):
        try:
            product = Product.objects.get(pk=productId)
            fullProductData = self._SerializeProductDetail(product)

            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data=fullProductData,
                message=ResponseMessage.PRODUCT_FETCHED_SUCCESS
                )
        except Product.DoesNotExist:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.NOT_FOUND,
                data={},
                message=ResponseMessage.PRODUCT_NOT_FOUND.replace("{}", str(productId))
                )
        except Exception as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.PRODUCT_FETCHED_ERROR
                )

    def SearchProducts(self, request: HttpRequest):
        try:
            querys = request.GET.get('querys', '')
            filters = Q()
            if querys:
                filterPairs = querys.split('|')
                for pair in filterPairs:
                    if ':' in pair:
                        filterType, valuesStr = pair.split(':', 1)
                        values = [v.strip() for v in valuesStr.split(',') if v.strip()]
                        if filterType == 'category':
                            filters &= Q(category__value__in=values)
                        elif filterType == 'dietryNeeds':
                            filters &= Q(dietryNeeds__value__in=values)

            filteredProducts = Product.objects.filter(filters).distinct().order_by('-id')

            # --- Pagination ---
            page = request.GET.get('page', 1)
            pageSize = request.GET.get('pageSize', 10)
            paginator = Paginator(filteredProducts, pageSize)
            products_page=[]
            products_page = paginator.page(page)   

            serializedData = self._SerializeProductList(products_page.object_list)

            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data={
                    "items": serializedData,
                    
                        "totalItems": paginator.count,
                        "totalPages": paginator.num_pages,
                        "currentPage": products_page.number,
                        "hasNext": products_page.has_next(),
                        "hasPrevious": products_page.has_previous(),
                    
                },
                message=ResponseMessage.PRODUCTS_FETCHED_SUCCESS
            )
        except Exception as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.PRODUCTS_FETCHED_ERROR
            )

    # --- Blog Functions ---

    def GetBlogs(self, request):
        try:
            allBlogs = Blog.objects.all().order_by('-id')

            page = request.GET.get('page', 1)
            pageSize = request.GET.get('pageSize', 10)
            paginator = Paginator(allBlogs, pageSize)
            blogs_page = paginator.page(page)

            serializedData = self._SerializeBlogList(blogs_page.object_list)

            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data={
                    "items": serializedData,
                    
                        "totalItems": paginator.count,
                        "totalPages": paginator.num_pages,
                        "currentPage": blogs_page.number,
                        "hasNext": blogs_page.has_next(),
                        "hasPrevious": blogs_page.has_previous(),
                    
                },
                message=ResponseMessage.BLOGS_FETCHED
            )
        except Exception as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.BLOGS_FETCHED_ERROR
            )


    def FilterBlogsByCategory(self, categoryId, request):
        try:
            category = BlogCategory.objects.get(pk=categoryId)
            filteredBlogs = Blog.objects.filter(category=category).order_by('-id')
            
            # --- Pagination ---
            page = request.GET.get('page', 1)
            pageSize = request.GET.get('pageSize', 10)

            paginator = Paginator(filteredBlogs, pageSize)
            blogs_page = paginator.page(page)
            

            serializedData = self._SerializeBlogList(blogs_page.object_list)

            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data={
                    "items": serializedData,
                    
                        "totalItems": paginator.count,
                        "totalPages": paginator.num_pages,
                        "currentPage": blogs_page.number,
                        "hasNext": blogs_page.has_next(),
                        "hasPrevious": blogs_page.has_previous(),
                    
                },
                message=ResponseMessage.BLOGS_FETCHED.replace("{}", str(category.label))
            )
        except BlogCategory.DoesNotExist as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.NOT_FOUND,
                data={"error": str(e)},
                message=ResponseMessage.BLOG_CATEGORY_NOT_FOUND.replace("{}", str(categoryId))
            )
        except Exception as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.BLOGS_FETCHED_ERROR
            )
    def GetBlogById(self, blogId):
        try:
            blog = Blog.objects.get(pk=blogId)
            fullBlogData = self._SerializeBlogDetail(blog)
            
            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data=fullBlogData,
                message=ResponseMessage.BLOG_FETCHED
                )
        except Blog.DoesNotExist:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.NOT_FOUND,
                data={},
                message=ResponseMessage.BLOG_NOT_FOUND.replace("{}", str(blogId))
                )
        except Exception as e:
            return localResponse(
                response=False,
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.BLOG_FETCHED_ERROR.replace("{}", str(blogId))
                )