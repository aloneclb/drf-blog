from rest_framework import serializers
from post.models import Post, Category, Tag, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id',
                'author',
                'title',
                'excerpt',
                'image',
                'content',
                'slug',
                'status',
                'category',
                'tags',
                ]
        read_only_fields = ['id', 'author']
                
    def validate(self, data):
        # Eğer gelen veride baslik ve açıklama değerleri aynıysa hata ver
        if data['title'] == data['excerpt']:
            raise serializers.ValidationError('Başlık ve giriş cümlesi alanları aynı olamaz. Lütfen farklı bir giriş cümlesi giriniz.')
        
        return data

    def validate_title(self, value):
        # Eğer baslik 3 harften küçükse hata ver
        if len(value) < 5: 
            raise serializers.ValidationError(f'Başlık 5 harften daha küçük olamaz. Siz {len(value)} girdiniz. Başlık alanınızı değiştiriniz.')

        return value    



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
    


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



class SinglePostReadSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id',
                'author',
                'title',
                'excerpt',
                'image',
                'content',
                'slug',
                'status',
                'category',
                'tags',
                'comments'
                ]
        read_only_fields = ['id', 'author', 'comments']
    

class SinglePostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id',
                'author',
                'title',
                'excerpt',
                'image',
                'content',
                'slug',
                'status',
                'category',
                'tags',
                'comments'
                ]
        read_only_fields = ['id', 'author', 'comments']
    
    def validate(self, data):
        # Eğer gelen veride baslik ve açıklama değerleri aynıysa hata ver
        if data['title'] == data['excerpt']:
            raise serializers.ValidationError('Başlık ve giriş cümlesi alanları aynı olamaz. Lütfen farklı bir giriş cümlesi giriniz.')
        
        return data

    def validate_title(self, value):
        # Eğer baslik 5 harften küçükse hata ver
        if len(value) < 5: 
            raise serializers.ValidationError(f'Başlık 5 harften daha küçük olamaz. Siz {len(value)} girdiniz. Başlık alanınızı değiştiriniz.')

        return value  