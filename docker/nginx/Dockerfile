FROM nginx:1.25-alpine

# Remove config padrão do nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia nossa config personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf
