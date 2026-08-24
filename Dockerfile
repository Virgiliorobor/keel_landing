# Trade Focus static site: / (manifesto) + /keel/ (product landing).
# Only the production pages are copied — concept archives stay out.
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY keel/index.html /usr/share/nginx/html/keel/index.html
EXPOSE 80
