require recipes-graphics/images/core-image-x11.bb
IMAGE_INSTALL += " strace \
                        gstreamer1.0 gstreamer1.0-plugins-imx-meta \
                        gstreamer1.0-plugins-base-meta gstreamer1.0-plugins-good-meta \
                        gstreamer1.0-plugins-bad-meta gstreamer1.0-plugins-good \
                        gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
                        gstreamer1.0-libav gstreamer1.0-plugins-base-playback \
                        gstreamer1.0-meta-base \
                        gstreamer1.0-meta-video \
                        gstreamer1.0-meta-audio \
                        gstreamer1.0-meta-debug \
                        gstreamer1.0-plugins-imx gstreamer1.0-plugins-ugly-meta \
                        pulseaudio pulseaudio-server \
                        alsa-utils alsa-utils-speakertest \
                        gst-fsl-plugin gst-ffmpeg\
                        gstreamer1.0-plugins-good-multifile-dev \
                        python-subprocess \
                        "
##removed packages
#                        python-gst
#                        rsync

COMMERCIAL_AUDIO_PLUGINS ?= " \
gst-plugins-ugly-mad \
gst-plugins-ugly-mpegaudioparse \
gst-fsl-plugin \
"
COMMERCIAL_VIDEO_PLUGINS ?= " \
gst-plugins-ugly-mpeg2dec \
gst-plugins-ugly-mpegstream \
gst-plugins-bad-mpegvideoparse \
"
CORE_IMAGE_EXTRA_INSTALL += " \
alsa-utils \
gst-ffmpeg \
gst-plugins-base-videotestsrc \
gst-plugins-bad-fbdevsink \
gst-plugins-good-isomp4 \
"

#PREFERRED_VERSION_gstreamer1.0 = "1.8.3"
#PREFERRED_VERSION_gstreamer1.0-plugins-base = "1.8.3"
#PREFERRED_VERSION_gstreamer1.0-plugins-good = "1.8.3"
#PREFERRED_VERSION_gstreamer1.0-plugins-bad = "1.8.3"
#PREFERRED_VERSION_gstreamer1.0-plugins-ugly = "1.8.3"
#PREFERRED_VERSION_gstreamer1.0-libav = "1.8.3"
#PREFERRED_VERSION_gstreamer1.0-omx = "1.8.3"

