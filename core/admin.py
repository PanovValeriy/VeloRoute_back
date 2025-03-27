from django.contrib import admin

from core.models import Author, TypeEvent, Tempo, Complexity, Route, Event, Report, VisitCount

admin.site.register(Author)
admin.site.register(TypeEvent)
admin.site.register(Tempo)
admin.site.register(Complexity)
admin.site.register(Route)
admin.site.register(Event)
admin.site.register(Report)
admin.site.register(VisitCount)
