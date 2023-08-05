from django.urls import path
# from api.views import BookReviewDetailAPIView,BookReviewsApiView
from rest_framework.routers import DefaultRouter
from api.views import BookReviewViewSet
router = DefaultRouter()

app_name = "api"

router.register('reviews', BookReviewViewSet, basename='review')

urlpatterns = router.urls

# urlpatterns = [
#     path("reviews/", BookReviewsApiView.as_view(), name='review-list'),
#     path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name='review-detail'),
# ]
