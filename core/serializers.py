from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from core.models import *
from user.serializers import UserNickNameSerializer


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ComplexitySerializer(ModelSerializer):
    class Meta:
        model = Complexity
        fields = ('id', 'name')


class TypeEventSerializer(ModelSerializer):
    class Meta:
        model = TypeEvent
        fields = '__all__'


class TempoSerializer(ModelSerializer):
    class Meta:
        model = Tempo
        fields = ('id', 'name')


class RouteSerializer(ModelSerializer):
    author = AuthorSerializer()
    complexity = ComplexitySerializer()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()

    class Meta:
        model = Route
        fields = '__all__'

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)


class RouteListSerializer(ModelSerializer):
    author = AuthorSerializer()
    complexity = ComplexitySerializer()
    viewsCount = SerializerMethodField()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()

    class Meta:
        model = Route
        fields = ('id', 'name', 'photoURL', 'length', 'asphalt', 'grader', 'soil', 'jungle', 'author', 'complexity', 'dateCreate', 'dateUpdate', 'viewsCount', 'likesCount', 'like')

    def get_viewsCount(self, obj):
        return getattr(obj, 'viewsCount', 0)

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)


class MemberSerializer(ModelSerializer):
    user = UserNickNameSerializer()

    class Meta:
        model = Members
        fields = ('user',)


class EventSerializer(ModelSerializer):
    author = AuthorSerializer()
    route = RouteSerializer()
    typeEvent = TypeEventSerializer()
    tempo = TempoSerializer()
    complexity = ComplexitySerializer()
    viewsCount = SerializerMethodField()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()
    membersCount = SerializerMethodField()
    member = SerializerMethodField()
    members_set = MemberSerializer(many=True, read_only=True)


    class Meta:
        model = Event
        fields = '__all__'

    def get_viewsCount(self, obj):
        return getattr(obj, 'viewsCount', 0)

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)

    def get_membersCount(self, obj):
        return getattr(obj, 'membersCount', 0)

    def get_member(self, obj):
        return getattr(obj, 'member', False)


class EventNotAuthSerializer(ModelSerializer):
    author = AuthorSerializer()
    route = RouteSerializer()
    typeEvent = TypeEventSerializer()
    tempo = TempoSerializer()
    complexity = ComplexitySerializer()
    viewsCount = SerializerMethodField()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()
    membersCount = SerializerMethodField()
    member = SerializerMethodField()
    members_set = SerializerMethodField()


    class Meta:
        model = Event
        fields = '__all__'

    def get_viewsCount(self, obj):
        return getattr(obj, 'viewsCount', 0)

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)

    def get_membersCount(self, obj):
        return getattr(obj, 'membersCount', 0)

    def get_member(self, obj):
        return getattr(obj, 'member', False)

    def get_members_set(self, obj):
        return []


class ReportSerializer(ModelSerializer):
    author = AuthorSerializer()
    route = RouteSerializer()
    event = EventSerializer()
    viewsCount = SerializerMethodField()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()

    class Meta:
        model = Report
        fields = '__all__'

    def get_viewsCount(self, obj):
        return getattr(obj, 'viewsCount', 0)

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)

class ReportListSerializer(ModelSerializer):
    author = AuthorSerializer()
    viewsCount = SerializerMethodField()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()

    class Meta:
        model = Report
        fields = ('id', 'date', 'name', 'photoURL', 'author', 'dateCreate', 'dateUpdate', 'viewsCount', 'likesCount', 'like')

    def get_viewsCount(self, obj):
        return getattr(obj, 'viewsCount', 0)

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)


class EventListSerializer(ModelSerializer):
    author = AuthorSerializer()
    typeEvent = TypeEventSerializer()
    tempo = TempoSerializer()
    complexity = ComplexitySerializer()
    viewsCount = SerializerMethodField()
    miniReportTrue = SerializerMethodField()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()
    membersCount = SerializerMethodField()
    member = SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'author', 'name', 'typeEvent', 'length', 'tempo', 'startDateTime', 'startPlace', 'complexity', 'photoURL', 'dateCreate', 'dateUpdate', 'viewsCount', 'miniReportTrue', 'likesCount', 'like', 'membersCount', 'member')

    def get_viewsCount(self, obj):
        return getattr(obj, 'viewsCount', 0)

    def get_miniReportTrue(self, obj):
        return bool(getattr(obj, 'miniReport', ''))

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)

    def get_membersCount(self, obj):
        return getattr(obj, 'membersCount', 0)

    def get_member(self, obj):
        return getattr(obj, 'member', False)


class InfoListSerializer(ModelSerializer):
    viewsCount = SerializerMethodField()
    likesCount = SerializerMethodField()
    like = SerializerMethodField()

    class Meta:
        model = Info
        fields = ('id', 'name', 'body', 'priority', 'dateCreate', 'dateUpdate', 'viewsCount', 'likesCount', 'like')

    def get_viewsCount(self, obj):
        return getattr(obj, 'viewsCount', 0)

    def get_likesCount(self, obj):
        return getattr(obj, 'likesCount', 0)

    def get_like(self, obj):
        return getattr(obj, 'like', False)


class InfoSerializer(ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'

