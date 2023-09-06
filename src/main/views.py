import sys
import traceback

import pdfkit
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_exempt

from logger import err_logger, logger
from main.auth import validate_request
from main.forms import FileForm
from main.models import Graph
from processor.gpAUDITEXAMEN import (ProcessException, generate_graph,
                                     process_file)


def get_site(request):
    site = SimpleLazyObject(lambda: get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'
    return SimpleLazyObject(lambda: "{0}://{1}".format(protocol, site.domain))


@csrf_exempt
@transaction.atomic
def create_view(request):
    logger.debug('===== Request received =====')

    # Validate request
    if not validate_request(request):
        return JsonResponse({'error': "Not Authorized"}, status=401)


    # Extract file from request
    logger.debug('===== Validating file =====')
    form = FileForm(files=request.FILES)
    valid = form.is_valid()
    if not valid:
        return JsonResponse({'error': form.errors.as_text()}, status=400)
    
    logger.debug('===== Reading file =====')
    file: InMemoryUploadedFile = request.FILES.get('file')
    content = ""
    for _line in file:
        content += _line.decode("utf-8")

    # Process file
    processed = None
    try:
        logger.debug('===== Processing file =====')
        processed = process_file(str(content))
    except ProcessException as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=400)

    logger.debug('===== Creating Graph =====')
    # Generate images
    graph = Graph.objects.create()

    logger.debug('===== Generating Graph =====')

    graph_generator = generate_graph(processed, str(graph.id))
    data = graph_generator.generarPDF()
    graph.tablanotas = data['tablanotas']
    graph.tablaaudit = data['tablaaudit']
    graph.save()

    logger.debug('===== Generating PDF =====')

    # Save pdf to media use –user-style-sheet
    output = settings.BASE_DIR / 'media' / f'{graph.id}/result.pdf'
    rendered = render_to_string('main/index.html', {
        'graph': graph,
        'site': get_site(request),
    })

    config = None
    if sys.platform == "win32":
        config = pdfkit.configuration(
            wkhtmltopdf="C:\\Users\\Administrator\\Downloads\\wkhtmltox-0.12.6-1.mxe-cross-win64\\wkhtmltox\\bin\\wkhtmltopdf.exe")

    pdfkit.from_string(
        rendered, output,
        options={
            'enable-local-file-access': None,
            'user-style-sheet': settings.BASE_DIR / 'assets' / 'css' / 'informe.css'
        },
        configuration=config
    )

    abs_url = graph.get_absolute_url()
    return JsonResponse({'url': abs_url})


def result_view(request, graph_id: str):
    try:
        graph = Graph.objects.get(id=graph_id)
    except Graph.DoesNotExist:
        return render(
            request, 'main/error.html',
            {'content': 'Graph does not exist'}
        )
    return render(request, 'main/index.html', {'graph': graph, 'site': get_site(request)})
