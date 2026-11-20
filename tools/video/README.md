# مقطع أفق الذكاء (دقيقة، طولي 1080×1920)

طريقة إعادة توليد المقطع بعد أي تغيير في الموقع:

1. ابنِ الموقع العام وانسخه هنا باسم `site.html`.
2. صوّر الصفحات: `mkdir -p cap && node capture.js` ثم رحلة الصاروخ: `node flight.js` (ساعة الصفحة مجمّدة، والإطارات تتبع `times.json`). أوقات أحداث الرحلة في `events.json`، وإذا تغيرت الورشة شغّل `node scan.js` لقراءتها من جديد.
3. قص صور «وأكثر من ذلك»: صور sky وsolar وsaudi وquiz من y=104 إلى y=1104 باسم `cap/m-<الاسم>.jpg`.
4. جهّز صفحة المشهد: استبدل `LOGO` في `stage.src.html` بمحتوى `../brand/logo.svg`، و`LOGO2` بنفس المحتوى بعد تغيير `lg-` إلى `lh-`، واحفظها `stage.html`.
5. راجع لقطات مهمة: `node keyframes.js`.
6. الصوت: `python3 sfx.py` يصنع مؤثرات صوتية مربوطة بالمشاهد وبأحداث الرحلة (بدون موسيقى) في `sfx.wav`.
7. صيّر المقطع: `mkdir -p chunks && node render.js 0 1 2 3 4 5`، ثم اجمع المقاطع وأضف الموسيقى:
   `ffmpeg -f concat -safe 0 -i list.txt -c copy v.mp4` و`ffmpeg -i v.mp4 -i sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest ufuq-ai-promo.mp4`.

الصور والمقطع النهائي لا تُرفع للمستودع لأن حجمها كبير.
