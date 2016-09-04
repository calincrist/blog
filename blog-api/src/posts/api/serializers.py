from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
)

from posts.models import Post

post_detail_url = HyperlinkedIdentityField(
	view_name='posts-api:detail',
	lookup_field='slug'
)

class PostCreateUpdateSerializer(ModelSerializer):
	class  Meta:
		model = Post
		fields = [
			'title',
			'content',
			'publish'
		]

class PostDetailSerializer(ModelSerializer):
	url = post_detail_url
	image = SerializerMethodField()
	user = SerializerMethodField()
	html = SerializerMethodField()

	def get_user(self, obj):
		return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None

		return image

	def get_html(self, obj):
		return obj.get_markdown()

	class  Meta:
		model = Post
		fields = [
			'url',
			'user',
			'title',
			'content',
			'html',
			'image',
			'publish'
		]

class PostListSerializer(ModelSerializer):
	url = post_detail_url
	user = SerializerMethodField()
	image = SerializerMethodField()

	def get_user(self, obj):
		return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None

		return image

	class  Meta:
		model = Post
		fields = [
			'url',
			'user',
			'title',
			'content',
			'image',
			'publish'
		]
