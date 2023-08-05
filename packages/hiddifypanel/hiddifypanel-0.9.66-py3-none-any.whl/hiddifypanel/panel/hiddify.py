from flask import jsonify,g,url_for,Markup
from flask import flash as flask_flash
to_gig_d = 1000*1000*1000
import datetime

from hiddifypanel.panel.database import db
from hiddifypanel.models import StrConfig,BoolConfig,User,Domain,get_hconfigs,Proxy,hconfig,ConfigEnum,DomainType
import urllib
from flask_babelex import lazy_gettext as _
from flask_babelex import gettext as __
from hiddifypanel import xray_api
from sqlalchemy.orm import Load 

def add_temporary_access():
    import random

    random_port=random.randint(30000, 50000)
    exec_command(f'/opt/hiddify-config/hiddify-panel/temporary_access.sh {random_port} &')
    # iptableparm=f'PREROUTING -p tcp --dport {random_port} -j REDIRECT --to-port 9000'
    # exec_command(f'iptables -t nat -I {iptableparm}')
    # exec_command(f'echo "iptables -t nat -D {iptableparm}" | at now + 4 hour')
    
    # iptableparm=f'INPUT -p tcp --dport {random_port} -j ACCEPT'
    # exec_command(f'iptables -I {iptableparm}')
    # exec_command(f'echo "iptables -D {iptableparm}" | at now + 4 hour')

    temp_admin_link=f"http://{get_ip(4)}:{random_port}{get_admin_path()}"
    g.temp_admin_link=temp_admin_link
    

def get_admin_path():
    proxy_path=hconfig(ConfigEnum.proxy_path)
    admin_secret=hconfig(ConfigEnum.admin_secret)        
    return (f"/{proxy_path}/{admin_secret}/admin/")

def exec_command(cmd,cwd=None):
    try:
        import os
        os.system(cmd)
    except Exception as e:
        print(e)

    

def auth(function):
    def wrapper(*args,**kwargs):
        if g.user_uuid==None:
            return jsonify({"error":"auth failed"})
        if not admin and g.is_admin:
            return jsonify({"error":"admin can not access user page. add /admin/ to your url"})
    
        return function()

    return wrapper
def admin(function):
    def wrapper(*args,**kwargs):
        if g.user_uuid==None:
            return jsonify({"error":"auth failed"})
        if not g.is_admin:
            return jsonify({"error":"invalid admin"})
    
        return function()

    return wrapper

def abs_url(path):
    return f"/{g.proxy_path}/{g.user_uuid}/{path}"
def asset_url(path):
    return f"/{g.proxy_path}/{path}"

def update_usage():
        
        res={}
        have_change=False
        for user in User.query.all():
            if user.monthly and (datetime.date.today()-user.last_reset_time).days>=30:
                user.last_reset_time=datetime.date.today()
                if user.current_usage_GB > user.usage_limit_GB:
                    xray_api.add_client(user.uuid)
                    have_change=True
                user.current_usage_GB=0

            d = xray_api.get_usage(user.uuid,reset=True)
            
            if d == None:
               res[user.uuid]="No value" 
            else:
                in_gig=(d)/to_gig_d
                res[user.uuid]=in_gig
                user.current_usage_GB += in_gig
            if user.current_usage_GB > user.usage_limit_GB:
                xray_api.remove_client(user.uuid)
                have_change=True
                res[user.uuid]+=" !OUT of USAGE! Client Removed"
                    
        db.session.commit()
        if have_change:
            quick_apply_users()
        return {"status": 'success', "comments":res}
        

def domain_dict(d):
    return {
            'domain':d.domain,
            'mode':d.mode,
            'cdn_ip':d.cdn_ip,
            'show_domains':[dd.domain for dd in d.show_domains]
        }

def all_configs():
    configs={
        "users": [u.to_dict() for u in User.query.filter((User.usage_limit_GB>User.current_usage_GB)).filter(User.expiry_time>=datetime.date.today()).all()],
        "domains": [domain_dict(u) for u in Domain.query.all()],
        "hconfigs": get_hconfigs()
        }
    for d in configs['domains']:
        d['domain']=d['domain'].lower()
        # del d['domain']['show_domains']

    return configs
    

def get_ip(version,retry=3):
    try:
        return urllib.request.urlopen(f'https://v{version}.ident.me/').read().decode('utf8')
    except:
        if retry==0:
            return None
        return get_ip(version,retry=retry-1)


def get_available_proxies():
    proxies=Proxy.query.all()
    
    if not hconfig(ConfigEnum.domain_fronting_domain):
        proxies=[c for c in proxies if 'Fake' not in c.cdn]
    if not hconfig(ConfigEnum.ssfaketls_enable):
        proxies=[c for c in proxies if 'faketls' != c.transport]
        proxies=[c for c in proxies if 'v2ray' != c.proto]
    if not hconfig(ConfigEnum.shadowtls_enable):
        proxies=[c for c in proxies if c.transport!='shadowtls']
    if not hconfig(ConfigEnum.ssr_enable):
        proxies=[c for c in proxies if 'ssr' != c.proto]
    if not hconfig(ConfigEnum.vmess_enable):
        proxies=[c for c in proxies if 'vmess' not in c.proto]

    if not hconfig(ConfigEnum.kcp_enable):
        proxies=[c for c in proxies if 'kcp' not in c.l3]
    
    if not hconfig(ConfigEnum.http_proxy_enable):
        proxies=[c for c in proxies if 'http' != c.l3]
    
    if not Domain.query.filter(Domain.mode==DomainType.cdn).first():
        proxies=[c for c in proxies if c.cdn!="CDN"]
    return proxies

def quick_apply_users():
    exec_command("/opt/hiddify-config/install.sh apply_users &")


def flash_config_success(restart_mode='',domain_changed=True):
    if restart_mode:
        url=url_for('admin.Actions:reinstall',complete_install=restart_mode=='reinstall',domain_changed=domain_changed)
        apply_btn=f"<a href='{url}' class='btn btn-primary form_post'>"+_("admin.config.apply_configs")+"</a>"
        flash((_('config.validation-success',link=apply_btn)), 'success')
    else:
        flash((_('config.validation-success-no-reset')), 'success')

# Importing socket library 
import socket 

# Function to display hostname and 
# IP address 
def get_domain_ip(domain): 
    import socket
    try: 
        return socket.gethostbyname(domain) 
    except: 
        try:
            return socket.getaddrinfo(domain, None, socket.AF_INET6);
        except: 
            return None



def get_user_link(uuid,domain,mode=''):
        proxy_path=hconfig(ConfigEnum.proxy_path)
        res=""
        if mode=="multi":
            res+="<div class='btn-group'>"

        link=f"https://{domain.domain}/{proxy_path}/{uuid}/"
        link_multi=f"{link}multi"
        if mode=='new':
            link=f"{link}new"
        text= domain.domain
        if domain.mode==DomainType.cdn:
            text=f'<span class="badge badge-success" >{_("domain.cdn")}</span>'+text
        
        if mode=="multi":
            res+=f"<a class='btn btn-xs btn-secondary' target='_blank' href='{link_multi}' >{_('all')}</a>"
        res+=f"<a target='_blank' href='{link}' class='btn btn-xs btn-info ltr' ><i class='fa-solid fa-arrow-up-right-from-square'></i> {text}</a>"


        if mode=="multi":
            res+="</div>"
        return res



def flash(message,category):
    print(message)
    return flask_flash(Markup(message),category)





def validate_domain_exist(form,field):
        domain=field.data
        if not domain:return
        dip=get_domain_ip(domain)
        if dip==None:
                raise ValidationError(_("Domain can not be resolved! there is a problem in your domain"))
        


def check_need_reset(old_configs):
    restart_mode=''
    for c in old_configs:
        if old_configs[c]!=hconfig(c) and c.apply_mode():
            if restart_mode!='reinstall':
                restart_mode=c.apply_mode()
    # do_full_install=old_config[ConfigEnum.telegram_lib]!=hconfig(ConfigEnum.telegram_lib)
    
    flash_config_success(restart_mode=restart_mode,domain_changed=False)
    