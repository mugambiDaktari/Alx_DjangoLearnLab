from rest_framework import serializers
from .models import Book, Author
from datetime import datetime
from .models import Book, Author  # Import the models to serialize
from datetime import datetime  # Import datetime to check the current year

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    - Converts Book model instances to JSON format and vice versa.
    - Includes a custom validation method to ensure `publication_year` is not in the future.
    """

    class Meta:
        """
        Meta class defining model and fields to be serialized.
        
        - `model = Book`: Specifies that this serializer is for the Book model.
        - `fields = '__all__'`: Includes all fields from the Book model in the serialized output.
        """
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Custom validation for `publication_year`.
        
        - Ensures that the publication year is not set in the future.
        - If `publication_year` is greater than the current year, raises a ValidationError.
        - Returns the valid `publication_year` if it meets the condition.
        """
        current_year = datetime.now().year  # Get the current year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value  # Return the validated publication year


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    - Serializes Author instances along with their related books.
    - Uses the BookSerializer to display books written by the author.
    - The `books` field is read-only, meaning it will not be used for creating or updating an author.
    """
    books = BookSerializer(many=True, read_only=True)  # Serializes related books

    class Meta:
        """
        Meta class defining model and fields to be serialized.
        
        - `model = Author`: Specifies that this serializer is for the Author model.
        - `fields = ['name', 'books']`: Includes only the author's name and their related books.
        """
        model = Author
        fields = ['name', 'books']
