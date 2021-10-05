from django.core.files.base import ContentFile
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from hub.models import Hub
from note.models import (
    Note,
    NoteContent
)
from note.serializers import NoteSerializer, NoteContentSerializer
from researchhub_access_group.models import ResearchhubAccessGroup, Permission
from researchhub_document.models import (
    ResearchhubUnifiedDocument
)
from researchhub_document.related_models.constants.document_type import (
    NOTE
)
from user.models import Organization
from django.http import HttpResponse
from utils.http import RequestMethods
from jwt import encode
from datetime import datetime
from researchhub.settings import (
    CKEDITOR_CLOUD_ACCESS_KEY,
    CKEDITOR_CLOUD_ENVIRONMENT_ID
)


class NoteViewSet(ModelViewSet):
    ordering = ('-created_date')
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        organization_id = data.get('organization', None)
        title = data.get('title', '')

        if organization_id:
            created_by = None
            organization = Organization.objects.get(id=organization_id)
        else:
            created_by = user
            organization = None

        access_group = self._create_access_group(created_by, organization)
        unified_doc = self._create_unified_doc(request, access_group)
        note = Note.objects.create(
            created_by=created_by,
            organization=organization,
            unified_document=unified_doc,
            title=title,
        )
        serializer = self.serializer_class(note)
        data = serializer.data
        return Response(data, status=200)

    def _create_unified_doc(self, request, access_group):
        data = request.data
        hubs = Hub.objects.filter(
            id__in=data.get('hubs', [])
        ).all()
        unified_doc = ResearchhubUnifiedDocument.objects.create(
            document_type=NOTE
        )
        unified_doc.access_group.add(access_group)
        unified_doc.hubs.add(*hubs)
        unified_doc.save()
        return unified_doc

    def _create_access_group(self, creator, organization):
        if organization:
            access_group = organization.access_group
            return access_group

        access_group = ResearchhubAccessGroup.objects.create()
        Permission.objects.create(
            access_group=access_group,
            user=creator,
            access_type=Permission.ADMIN
        )
        return access_group

    def _get_context(self):
        context = {
        }
        return context

    @action(
        detail=True,
        methods=['get'],
    )
    def get_organization_notes(self, request, pk=None):
        user = request.user

        if pk == '0':
            notes = self.queryset.filter(
                created_by__id=user.id,
                unified_document__is_removed=False,
            )
        else:
            notes = self.queryset.filter(
                organization__id=pk,
                unified_document__is_removed=False,
            )

        serializer = self.serializer_class(notes, many=True)
        return Response(serializer.data, status=200)

    @action(
        detail=True,
        methods=['post'],
    )
    def delete(self, request, pk=None):
        note = self.queryset.get(id=pk)
        unified_document = note.unified_document
        unified_document.is_removed = True
        unified_document.save()
        serializer = self.serializer_class(note)
        return Response(serializer.data, status=200)


class NoteContentViewSet(ModelViewSet):
    ordering = ('-created_date')
    queryset = NoteContent.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NoteContentSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        src = data.get('full_src', '')
        note = data.get('note', None)
        plain_text = data.get('plain_text', None)

        note_content = NoteContent.objects.create(
            note_id=note,
            plain_text=plain_text
        )
        file_name, file = self._create_src_content_file(
            note_content,
            src,
            user
        )
        note_content.src.save(file_name, file)
        serializer = self.serializer_class(note_content)
        data = serializer.data
        return Response(data, status=200)

    def _create_src_content_file(self, note, data, user):
        file_name = f'NOTE-CONTENT-{note}--USER-{user.id}.txt'
        full_src_file = ContentFile(data.encode())
        return file_name, full_src_file


@api_view([RequestMethods.GET])
@permission_classes([IsAuthenticated])
def ckeditor_token(request):
    user = request.user

    payload = {
        'aud': CKEDITOR_CLOUD_ENVIRONMENT_ID,
        'iat': datetime.utcnow(),
        'sub': f'user-{user.id}',
        'user': {
            'email': user.email,
            'name': f'{user.first_name} {user.last_name}',
            'avatar': user.author_profile.profile_image.url,
        },
        'auth': {
            'collaboration': {
                '*': {
                    'role': 'writer'
                }
            }
        },
    }

    encoded = encode(payload, CKEDITOR_CLOUD_ACCESS_KEY, algorithm='HS256')
    return HttpResponse(encoded)
