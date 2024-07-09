
from rest_framework.serializers import ModelSerializer
from users.models import PlatformUser, Post

class PlatFormUserSerializer(ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'username', 'is_superuser', 'is_staff')
        extra_kwargs = {'password': {'write_only': True},'username':{'read_only':True}}

    def validate(self, attrs):
        attrs['username'] = attrs['email']
        return attrs
    
    def create(self, validated_data):
        if validated_data.get('is_superuser',False):
            user = PlatformUser.objects.create_superuser(**validated_data)
        else:
            user = PlatformUser.objects.create_user(**validated_data)
        return user

       

class PlatFormUserUpdateSerializer(ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = ['first_name', 'last_name', 
                  'is_staff', 'is_active']
        
    def update(self, instance, validated_data):
        
        return super().update(instance, validated_data) 
    

class PostCreateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class PostSerializer(ModelSerializer):
    created_by = PlatFormUserUpdateSerializer()
    class Meta:
        model = Post
        fields = '__all__'