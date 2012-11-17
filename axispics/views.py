import os
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/axispics.pt')
def home_view(request):
    return {'project':'axis-pics'}

@view_config(route_name='pics')
def pics_view(request):
    settings = request.registry.settings
    dest_dir = settings['axis_pic_path']
    headers = request.headers
    headers = dict(headers)
    contd = headers['Content-Disposition']
    filename = contd.rsplit('"')[1]
    ip = request.remote_addr
    dest_path = '%s/%s/' % (dest_dir, ip)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    ofile = open(dest_path + filename, 'wb')

    filedata = request.body_file
    #filedata = request.body_file_seekable
    infile = filedata.read()
    ofile.write(infile)
    ofile.close()
    return Response('OK')
