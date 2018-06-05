from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from .models import Note as NoteModel

class Note(DjangoObjectType):
  class Meta:
      model = NoteModel

      # Describe the data as a node in the graph for GraphQL
      interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
  notes = graphene.List(Note)

  def resolve_notes(self, info):
    """Decide which notes to return."""

    user = info.context.user # Use docs or debugger to find

    if settings.DEBUG:
      return NoteModel.objects.all()
    elif user.is_anonymous:
      return NoteModel.objects.none()
    else:
      return NoteModel.objects.filter(user=user)

# Mutations
class CreateNote(graphene.Mutation):
    title = graphene.String()
    content = graphene.String()

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    # Output
    ok = graphene.Boolean()
    note = graphene.Field(Note)

    def mutate(self, info, title, content):
        user = info.context.user


        if user.is_anonymous:
          is_ok = False
          return CreateNote(ok=is_ok)

        else:
          note = NoteModel(title=title, content=content, user=user)
          note.save()
          is_ok = True

        return CreateNote(
            # title=note.title,
            # content=note.content,
            note=note, 
            ok=is_ok
        )

class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()

# Add a schema and attach the query
schema = graphene.Schema(query=Query, mutation=Mutation)