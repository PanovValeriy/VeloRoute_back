from rest_framework.serializers import ModelSerializer
from core.models import *


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

    class Meta:
        model = Route
        fields = '__all__'


class RouteListSerializer(ModelSerializer):
    author = AuthorSerializer()
    complexity = ComplexitySerializer()

    class Meta:
        model = Route
        fields = ('id', 'name', 'photoURL', 'length', 'asphalt', 'grader', 'soil', 'jungle', 'author', 'complexity')


class EventSerializer(ModelSerializer):
    author = AuthorSerializer()
    route = RouteSerializer()
    typeEvent = TypeEventSerializer()
    tempo = TempoSerializer()
    complexity = ComplexitySerializer()

    class Meta:
        model = Event
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    author = AuthorSerializer()
    route = RouteSerializer()
    event = EventSerializer()

    class Meta:
        model = Report
        fields = '__all__'


class ReportListSerializer(ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Report
        fields = ('id', 'date', 'name', 'photoURL', 'author')


class EventSerializer(ModelSerializer):
    author = AuthorSerializer()
    route = RouteSerializer()
    typeEvent = TypeEventSerializer()
    tempo = TempoSerializer()
    complexity = ComplexitySerializer()

    class Meta:
        model = Event
        fields = '__all__'


class EventListSerializer(ModelSerializer):
    author = AuthorSerializer()
    typeEvent = TypeEventSerializer()
    tempo = TempoSerializer()
    complexity = ComplexitySerializer()

    class Meta:
        model = Event
        fields = ('id', 'author', 'name', 'typeEvent', 'length', 'tempo', 'startDateTime', 'startPlace', 'complexity', 'photoURL')
