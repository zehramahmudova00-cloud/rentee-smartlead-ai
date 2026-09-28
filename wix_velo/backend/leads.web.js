import { Permissions, webMethod } from 'wix-web-module';
import { secrets } from 'wix-secrets-backend.v2';
import { elevate } from 'wix-auth';
import { fetch } from 'wix-fetch';

// Yönetim panelindeki kişisel bilgiler yalnızca site yöneticilerine açılır.
const getSecret = elevate(secrets.getSecretValue);
const API = 'https://rentee-smartlead-ai.onrender.com/api';

export const tumLeadler = webMethod(Permissions.Admin, async () => {
  const token = await getSecret('RENTEE_ADMIN_TOKEN');
  const response = await fetch(`${API}/leads`, {
    headers: { 'X-Admin-Token': token }
  });
  if (!response.ok) throw new Error('Lead kayıtları getirilemedi.');
  return response.json();
});
