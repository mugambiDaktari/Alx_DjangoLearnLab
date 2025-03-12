from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


# Create your views here.
class BookListViews(generics.ListCreateAPIView):
    """
    API endpoint to list all books or create a new book.
    
    - Inherits from ListCreateAPIView to provide default list and create behavior.
    - `queryset` specifies the list of books to display.
    - `serializer_class` specifies the serializer to use for book objects.
    """
    queryset = Book.objects.all()  # Get all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert books to JSON
    permission_classes = [permissions.AllowAny]  # Allow any user to access this endpoint

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()  # Get all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert books to JSON
    permission_classes = [permissions.AllowAny]  # Allow any user to access this endpoint

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()  # Get all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert books to JSON
    permission_classes = [permissions.IsAuthenticated]  # Allow only authenticated users to create books

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.perform_create(serializer)  # Perform custom creation logic
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the serialized data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()  # Get all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert books to JSON
    permission_classes = [permissions.IsAuthenticated]  # Allow only authenticated users to update books

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # allow partial updates
        instance = self.get_object() # get the book instance
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)  # Perform custom update logic
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return the serialized data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 
    filter_backends = [SearchFilter, OrderingFilter] # Enable search and ordering filters
    search_fields = ['title', 'publication_year'] # Allow searching by title and publication year
    ordering_fields = ['title', 'author'] # Allow ordering by title, and author.
    

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()  # Get all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert books to JSON
    permission_classes = [permissions.IsAuthenticated]  # Allow only authenticated users to delete books