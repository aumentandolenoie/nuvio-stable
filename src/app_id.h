#ifndef NV_APP_ID_H
#define NV_APP_ID_H
/* Package metadata and the runtime must be built with the same identity. */
#define NV_APP_ID_PRODUCTION "space.nuvio.native.legacy"
#ifndef NV_APP_ID
#ifdef NV_DTS_DEBUG
#error "NV_DTS_DEBUG requires an isolated NV_APP_ID package identity"
#endif
// Nuvio Stable is a separately installable LG webOS application.
// Keep the upstream production constant for data-directory isolation.
#define NV_APP_ID "space.nuvio.native.stable"
#endif
#ifdef NV_APP_ID_DEFAULT
#define NV_LS_MEDIA_CLIENT "com.webos.media.client.nuvio"
#else
#define NV_LS_MEDIA_CLIENT "com.webos.media.client." NV_APP_ID
#endif
#endif
