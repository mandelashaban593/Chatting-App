from remitapi.tasks import send_email, send_sms
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.template import RequestContext
import sys
from datetime import datetime


def mailer(request, subject, template, content, to, sender=False):
    if settings.DISABLE_COMMS:
        return True
    if not sender:
        sender = "%s via %s" % (settings.APP_NAME, settings.APP_EMAILS['info'])
    try:
        content['STATIC_URL'] = "%semail/" % settings.STATIC_URL
        html_content = render_to_string(
            template, content, context_instance=RequestContext(request))
        # this strips the html, so people will have the text as well.
        text_content = strip_tags(html_content)
        # create the email, and attach the HTML version as well.
        send_email(subject, text_content, sender, to, html_content)
    except Exception, e:
        print e
    return True


def send_msg_notification(msg, request):
    if msg.is_note:
        template = settings.EMAIL_TEMPLATE_DIR + 'new_note.html'
    else:
        template = settings.EMAIL_TEMPLATE_DIR + 'new_message.html'
    data = {'msg': msg}
    email = False
    subject = "New Message from 199Fix"
    try:
        email = msg.recipient.email
        if not subject:
            subject = '%s via 199Fix' % msg.sender_profile().short_name
    except Exception, e:
        print e
    mailer(request, subject, template, data, email)


def send_job_notification(job, request):
    if not job.status == '1':
        template = settings.EMAIL_TEMPLATE_DIR + 'new_job_status.html'
    else:
        template = settings.EMAIL_TEMPLATE_DIR + 'job.html'
    data = {'job': job}
    email = False
    subject = "%s via 199Fix [ %s ]" % (
        job.app.owner_profile().short_name,
        job.name
    )
    try:
        email = job.app.user.email
    except Exception:
        pass
    if not email:
        email = "madradavid@gmail.com"
    mailer(request, subject, template, data, email)


def debug(e, txt=False, log='debug'):
    txt = "%s %s" % (e, txt)
    if settings.DEBUG_API:
        if not txt:
            txt = ''
        print >> sys.stderr, 'Debuging____________________ %s' % txt
        print >> sys.stderr, e
    else:
        try:
            old_stdout = sys.stdout
            log_file = open("%slogs/%s.log" % (settings.LOG_DIR, log), "a")
            sys.stdout = log_file
            print '%s: Debuging_____________%s' % (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                txt
            )
            sys.stdout = old_stdout
            log_file.close()
        except Exception, e:
            print e


def balance_low_email(request, wallet, transaction):
    '''
    balance is low
    '''
    template = settings.EMAIL_TEMPLATE_DIR + 'balance_low_email.html'
    data = {'transaction': transaction}
    email = "stone@eversend.co.ug"
    subject = "Balance for %s is low" % wallet
    mailer(request, subject, template, data, email)


def error_message(request, msgtype, data={}):
    template = settings.BASE_DIR + 'templates/error_messages.html'
    data['type'] = msgtype
    text = render_to_string(
        template, data, context_instance=RequestContext(request))
    messages.error(request, text)


def success_message(request, msgtype, data={}):
    template = settings.BASE_DIR + 'templates/success_messages.html'
    data['type'] = msgtype
    text = render_to_string(
        template, data, context_instance=RequestContext(request))
    messages.success(request, text)


def admin_mail(request, code, data=False, e=False):
    '''admin email template'''
    template = settings.EMAIL_TEMPLATE_DIR + 'admin.html'
    subjects = {
        'pending_transaction': 'Pending Transaction',
        'complete_transaction': 'Transaction Complete',
        'user_verification': 'User Pending Verification',
        'user_verification_update': 'User Updated Verification Details',
        'new_user': '',
        'rates_error': 'An error occurred while fetching the rates',
        'server_error': 'Dude your App Just Broke',
        'contact_us': 'New Contact Message',
    }
    if settings.DEBUG:
        emails = settings.DEBUG_EMAILS
    if code == 'server_error':
        emails = {'madradavid@gmail.com'}
    elif code == 'contact_us':
        emails = {'info@remit.ug'}
    else:
        emails = {'atwine@gmail.com'}
    response = False
    if code in subjects:
        #emails = {'madra@redcore.co.ug'}
        subject = subjects[code]
        extradata = {}
        extradata['data'] = data
        extradata['code'] = code
        # if e:
        #    extradata['e'] = repr(e)
        sender = settings.APP_EMAILS['info']
        if 'contact_us' in subjects:
            sender = settings.APP_EMAILS['contact_us']
        for email in emails:
            response = mailer(request, subject, template,
                              extradata, email, sender)
    return response


def sendsms(to, template, content):
    '''backward compatibility ,move this to tasks.py'''
    return send_sms(to, template, content)
    # return True

COUNTRY_CHOICES = (
    ('UG', 'Uganda'),
    ('KE', 'Kenya'),
    ('TZ', 'Tanzania'),
    ('RW', 'Rwanda'),
)


NETWORK_CHOICES = (
    ('MTN', 'MTN Mobile Money'),
    ('AIRTEL', 'Airtel Money'),
    ('UTL', 'M-Sente'),
)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    #data = html.encode("ISO-8859-1")
    data = html.encode('utf-8')
    pdf = pisa.pisaDocument(StringIO.StringIO(data), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def log_unauthorized_access(request):
    debug(request, 'log_unauthorized_access')


def insufficient_account_balance(transaction):
    print "insufficient_account_balance"
