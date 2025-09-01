# Django Celery Deployment Guide for Render

## Step-by-Step Deployment Process

### 1. Prepare Your Repository

1. **Push your code to GitHub** with all the configuration files provided
2. **Ensure your project structure** looks like this:
   \`\`\`
   your-project/
   ├── myproject/
   │   ├── __init__.py
   │   ├── settings/
   │   │   ├── __init__.py
   │   │   ├── base.py
   │   │   └── production.py
   │   ├── celery.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── api/
   │   ├── __init__.py
   │   ├── tasks.py
   │   ├── views.py
   │   └── urls.py
   ├── render.yaml
   ├── build.sh
   ├── requirements.txt
   └── manage.py
   \`\`\`

### 2. Deploy to Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Click "New +" → "Blueprint"**
3. **Connect your GitHub repository**
4. **Render will automatically detect the `render.yaml` file**
5. **Review the services that will be created:**
   - Web Service (Django app)
   - Worker Service (Celery worker)
   - Worker Service (Celery beat - optional)
   - PostgreSQL Database
   - Redis Instance

### 3. Configure Environment Variables

Render will automatically set most environment variables, but you may need to add:

1. **EMAIL_HOST_USER**: Your email address
2. **EMAIL_HOST_PASSWORD**: Your email app password
3. **Any custom environment variables** your app needs

### 4. Monitor Deployment

1. **Watch the build logs** for each service
2. **Ensure all services start successfully**
3. **Check that migrations run correctly**

### 5. Test Your Deployment

#### Test API Endpoints:
\`\`\`bash
# Health check
curl https://your-app.onrender.com/api/health/

# Send email (test Celery)
curl -X POST https://your-app.onrender.com/api/send-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Email",
    "message": "This is a test email from Celery",
    "recipients": ["test@example.com"]
  }'
\`\`\`

#### Access Swagger Documentation:
- **Swagger UI**: `https://your-app.onrender.com/swagger/`
- **ReDoc**: `https://your-app.onrender.com/redoc/`

### 6. Verify Celery is Working

1. **Check Celery worker logs** in Render dashboard
2. **Send a test email** via the API
3. **Monitor task execution** in the logs
4. **Verify emails are being sent**

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check `build.sh` permissions: `chmod +x build.sh`
   - Verify all dependencies in `requirements.txt`

2. **Database Connection Issues**:
   - Ensure `DATABASE_URL` is properly set
   - Check PostgreSQL service is running

3. **Celery Worker Issues**:
   - Verify `REDIS_URL` is set correctly
   - Check worker service logs
   - Ensure Celery app is properly configured

4. **Email Issues**:
   - Use app-specific passwords for Gmail
   - Check email environment variables
   - Verify SMTP settings

### Monitoring:

- **Application Logs**: Available in Render dashboard
- **Celery Logs**: Check worker service logs
- **Database Logs**: Monitor PostgreSQL service
- **Redis Logs**: Check Redis service status

## Production Considerations

1. **Security**:
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS` properly
   - Enable HTTPS (Render provides this automatically)

2. **Performance**:
   - Monitor Celery worker performance
   - Scale workers based on task load
   - Use Redis for caching if needed

3. **Monitoring**:
   - Set up error tracking (Sentry)
   - Monitor application performance
   - Set up alerts for critical failures

## Scaling

- **Web Service**: Increase instance count in Render
- **Celery Workers**: Add more worker services
- **Database**: Upgrade PostgreSQL plan if needed
- **Redis**: Upgrade Redis plan for more memory
