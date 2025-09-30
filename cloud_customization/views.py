from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import datetime
import os
import subprocess
import tempfile
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class DatabaseBackupAPIView(APIView):

    def get(self, request):
        try:
            provided_password = request.GET.get("backup_password")
            password_token = os.environ.get("DATABASE_BACKUP_TOKEN", False)
            if not provided_password:
                print("No backup password provided.")
                logger.warning("No backup password provided.")
                return Response({"status": "error", "message": "Backup password is required"}, status=400)
            if not password_token:  
                print("No backup password token set in environment variables.")
                logger.warning("No backup password token set in environment variables.")
                return Response({"status": "error", "message": "Backup password token is not set"}, status=500)
            if  provided_password != password_token:
                print(f"Provided password: {provided_password}")
                print(f"Expected password token: {password_token}")
                logger.warning("Invalid backup password provided.")
                return Response({"status": "error", "message": "Invalid backup password"}, status=403)
            with tempfile.NamedTemporaryFile(suffix='.dump', delete=False) as temp_file:
                backup_path = temp_file.name

            db_config = settings.DATABASES['default']

            pg_dump_cmd = [
                'pg_dump',
                '--host', db_config['HOST'],
                '--port', str(db_config['PORT']),
                '--username', db_config['USER'],
                '--dbname', db_config['NAME'],
                '--file', backup_path,
                '--format=custom',
                '--compress=9',
                '--verbose',
                '--no-password'
            ]

            env = os.environ.copy()
            env['PGPASSWORD'] = db_config['PASSWORD']

            result = subprocess.run(
                pg_dump_cmd,
                env=env,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                logger.error(f"pg_dump failed: {result.stderr}")
                raise Exception(f"Backup failed: {result.stderr}")

            with open(backup_path, 'rb') as backup_file:
                backup_data = backup_file.read()

            os.unlink(backup_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'db_backup_{db_config["NAME"]}_{timestamp}.dump'
            response = HttpResponse(
                backup_data,
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(backup_data)

            return response

        except Exception as e:
            logger.error(f"Database backup failed: {str(e)}")
            return Response(
                {"error": f"Backup failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
#
class CloudOrganizationView(LoginRequiredMixin, View):
    def get(self, request):
        # Example: Replace this with actual subscription check logic
        if request.user.is_superuser:
            subscription_date = os.environ.get('SUBSCRIPTION_END_DATE')
            subscription_link =  os.environ.get('SUBSCRIPTION_VIEW_LINK')
            current_date  = datetime.date.today()
            subscription_date_end_date = datetime.datetime.strptime(subscription_date,'%Y-%m-%d').date()
            days_remaining = (subscription_date_end_date - current_date).days
            if days_remaining <=7:
                return JsonResponse({'validity': days_remaining,'subscription_link':subscription_link})
        return JsonResponse({'validity': None})
    