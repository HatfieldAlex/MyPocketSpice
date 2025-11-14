# Troubleshooting 404 Errors

## Quick Fix: Enable Mock Mode (Temporary)

If the backend isn't deployed yet, you can test the frontend with mock data:

1. Create a `.env` file in `frontend/my-pocket-spice/` (if it doesn't exist)
2. Add this line:
   ```
   VUE_APP_USE_MOCK=true
   ```
3. Restart the dev server (`npm run serve`)

This will use mock data instead of calling the backend.

## Debugging Steps

### 1. Check Browser Console
Open your browser's developer console (F12) and look for:
- `[API Config]` logs showing the base URL
- `[HTTP Client]` logs showing the exact URLs being called
- `[Backend Test]` logs showing connection test results

### 2. Verify Backend is Deployed
The backend needs to be deployed with:
- ✅ `backend/core/auth_views.py` (authentication views)
- ✅ `backend/core/auth_serializers.py` (authentication serializers)
- ✅ `backend/core/urls.py` (with auth routes included)
- ✅ Database migrations run (`python manage.py migrate`)

### 3. Test Backend Directly
Try accessing these URLs directly in your browser:
- `https://my-pocket-spice-backend.onrender.com/api/recipes/` (should return recipe list)
- `https://my-pocket-spice-backend.onrender.com/api/auth/register/` (will return 405 Method Not Allowed for GET, but confirms endpoint exists)

### 4. Check Backend Logs
On Render.com, check your backend service logs to see if:
- The service is running
- There are any errors during startup
- Requests are reaching the backend

## Common Issues

### Issue: "HTTP error! status: 404"
**Cause**: Backend endpoint doesn't exist or backend isn't deployed with auth routes.

**Solution**: 
1. Ensure backend code includes auth routes in `backend/core/urls.py`
2. Deploy the backend to Render.com
3. Verify migrations are run on Render.com

### Issue: CORS errors
**Cause**: Backend CORS settings not configured correctly.

**Solution**: Ensure `backend/config/settings.py` has:
```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

### Issue: Backend not reachable
**Cause**: Backend URL is wrong or service is down.

**Solution**: 
1. Check the base URL in `frontend/my-pocket-spice/src/api/config.ts`
2. Verify the backend service is running on Render.com
3. Check Render.com service logs

