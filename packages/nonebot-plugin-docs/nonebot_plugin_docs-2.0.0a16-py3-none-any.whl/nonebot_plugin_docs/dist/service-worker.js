/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a13.post1/advanced/export-and-require.html",
    "revision": "f0fbfc907de4712002c5b809be2655fd"
  },
  {
    "url": "2.0.0a13.post1/advanced/index.html",
    "revision": "de89863cf4c77323041390e507b5373e"
  },
  {
    "url": "2.0.0a13.post1/advanced/overloaded-handlers.html",
    "revision": "f7fd12b4ca43d6929cfdef45562ce2d2"
  },
  {
    "url": "2.0.0a13.post1/advanced/permission.html",
    "revision": "f396095d05eb6ba004ebfac62ad1836b"
  },
  {
    "url": "2.0.0a13.post1/advanced/publish-plugin.html",
    "revision": "9184c73a3de5fe005f08a510bd7a950f"
  },
  {
    "url": "2.0.0a13.post1/advanced/runtime-hook.html",
    "revision": "abcecb686f5dc0211b5e75991c979690"
  },
  {
    "url": "2.0.0a13.post1/advanced/scheduler.html",
    "revision": "277e7bc2d05c3782c9956479d02991be"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/cqhttp.html",
    "revision": "42108fa1be6b3c21303b695015cf2b14"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/ding.html",
    "revision": "3d1ce13d9f9fa00cb9647b0916cbec0b"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/index.html",
    "revision": "bec367eefb4610b840cc752d2b551f7b"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/mirai.html",
    "revision": "ed39019b8b757f417082c246b0f1e3c3"
  },
  {
    "url": "2.0.0a13.post1/api/config.html",
    "revision": "579668050dc4c8ba07b26ed4648f7634"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/fastapi.html",
    "revision": "046bee5f2fee2e028531e69fb87a9483"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/index.html",
    "revision": "ee59eace4d7825d9792ff2ac635cce85"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/quart.html",
    "revision": "c1a5853d362da8362561084dd8d10489"
  },
  {
    "url": "2.0.0a13.post1/api/exception.html",
    "revision": "a8e2102955ce55b525799d618f9e8790"
  },
  {
    "url": "2.0.0a13.post1/api/handler.html",
    "revision": "b0b70f3f41b5bc186494a2f24da26994"
  },
  {
    "url": "2.0.0a13.post1/api/index.html",
    "revision": "52f0a422c407e2fc7cadb6a11eaf0e17"
  },
  {
    "url": "2.0.0a13.post1/api/log.html",
    "revision": "b0351cfac9daca75ea0ee479c102de3c"
  },
  {
    "url": "2.0.0a13.post1/api/matcher.html",
    "revision": "be97dd65a860fc90313718ef92fb1993"
  },
  {
    "url": "2.0.0a13.post1/api/message.html",
    "revision": "438c2b47260ac53911b3ef2943626b37"
  },
  {
    "url": "2.0.0a13.post1/api/nonebot.html",
    "revision": "53edddba4d3cacf68b32b91847bfe1a3"
  },
  {
    "url": "2.0.0a13.post1/api/permission.html",
    "revision": "ca3acb9427e00f5df0a815d8f88897c5"
  },
  {
    "url": "2.0.0a13.post1/api/plugin.html",
    "revision": "73c14c81890919bbf1ea44e5e65e9f4a"
  },
  {
    "url": "2.0.0a13.post1/api/rule.html",
    "revision": "2818875b1ab7ae8e64bb60815d373a8b"
  },
  {
    "url": "2.0.0a13.post1/api/typing.html",
    "revision": "9600da21bf594acde26ea515feee54a0"
  },
  {
    "url": "2.0.0a13.post1/api/utils.html",
    "revision": "2eddc677eaf8175d859ab6293d2ec959"
  },
  {
    "url": "2.0.0a13.post1/guide/basic-configuration.html",
    "revision": "84acfe8051f5b97ff2f42574f4dd6005"
  },
  {
    "url": "2.0.0a13.post1/guide/cqhttp-guide.html",
    "revision": "d9977f1065b8cd7e3dcd79a05a1f3465"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-handler.html",
    "revision": "ca137ee3ee6dcbbe1951880066d7a4ea"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-matcher.html",
    "revision": "0c80f11115cd73eeef21b9c491da9139"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-plugin.html",
    "revision": "398a2e152fcad2e8add0cf581e147693"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-project.html",
    "revision": "ab9689d11735caae015ffc7b6009dcb1"
  },
  {
    "url": "2.0.0a13.post1/guide/ding-guide.html",
    "revision": "97e1068b1f3db415aa36e7913b8fd38d"
  },
  {
    "url": "2.0.0a13.post1/guide/end-or-start.html",
    "revision": "62db5a3fd31b4d24f6428c00bfc7a629"
  },
  {
    "url": "2.0.0a13.post1/guide/getting-started.html",
    "revision": "7d818329db464b7e8aff55503a26c4b8"
  },
  {
    "url": "2.0.0a13.post1/guide/index.html",
    "revision": "53260a0377c99b5dd09f814678ca97e7"
  },
  {
    "url": "2.0.0a13.post1/guide/installation.html",
    "revision": "42eda4c0d4cd1890cd162a545ce2521c"
  },
  {
    "url": "2.0.0a13.post1/guide/loading-a-plugin.html",
    "revision": "658a5951dfefb878da71fb2bddb5ab0c"
  },
  {
    "url": "2.0.0a13.post1/guide/mirai-guide.html",
    "revision": "f95442c4992fe7ba6fda69a1b8b69674"
  },
  {
    "url": "2.0.0a13.post1/index.html",
    "revision": "765d22990621f69dfea4ebc380570c33"
  },
  {
    "url": "2.0.0a15/advanced/export-and-require.html",
    "revision": "576f45883c96e75416dbe1ebbf2bf099"
  },
  {
    "url": "2.0.0a15/advanced/index.html",
    "revision": "e19c7b8d9ed02560cc056af93726e290"
  },
  {
    "url": "2.0.0a15/advanced/overloaded-handlers.html",
    "revision": "13310231a82d8532b25b4dc25a66ab91"
  },
  {
    "url": "2.0.0a15/advanced/permission.html",
    "revision": "37273bf13910cc8aae059906a3178bd0"
  },
  {
    "url": "2.0.0a15/advanced/publish-plugin.html",
    "revision": "dd4ef64a58a48e2182596f38e3e872cd"
  },
  {
    "url": "2.0.0a15/advanced/runtime-hook.html",
    "revision": "09091a97260e4a3927999af3701403b4"
  },
  {
    "url": "2.0.0a15/advanced/scheduler.html",
    "revision": "7786cb32c7aa18fa5f1a1f7a62191256"
  },
  {
    "url": "2.0.0a15/api/adapters/cqhttp.html",
    "revision": "a965a1de4c220a6133dd584796710607"
  },
  {
    "url": "2.0.0a15/api/adapters/ding.html",
    "revision": "c647b25661d6e59593b866836271a162"
  },
  {
    "url": "2.0.0a15/api/adapters/feishu.html",
    "revision": "afd1cbcc20e19bd3a7ab38ce6845ae04"
  },
  {
    "url": "2.0.0a15/api/adapters/index.html",
    "revision": "9538ddcc5785ba7a58cce0d584ad0c75"
  },
  {
    "url": "2.0.0a15/api/adapters/mirai.html",
    "revision": "9d7ccbddaed8db24127cc0d5a50d0910"
  },
  {
    "url": "2.0.0a15/api/config.html",
    "revision": "1943bb8942d213456af90ab16dbeb4a3"
  },
  {
    "url": "2.0.0a15/api/drivers/aiohttp.html",
    "revision": "a958b1352d66090140cb62024e2d1553"
  },
  {
    "url": "2.0.0a15/api/drivers/fastapi.html",
    "revision": "2e7da9756d34f43b941a68630c71c4e4"
  },
  {
    "url": "2.0.0a15/api/drivers/index.html",
    "revision": "423c6607d2d5f862a1f573ac2b686bb2"
  },
  {
    "url": "2.0.0a15/api/drivers/quart.html",
    "revision": "228ba80e5075df29d7751da169d73ea1"
  },
  {
    "url": "2.0.0a15/api/exception.html",
    "revision": "1ba1c1d6c18223c9d99c06169968da6d"
  },
  {
    "url": "2.0.0a15/api/handler.html",
    "revision": "42a912f5ae04ef276ba2445d4ff11cb5"
  },
  {
    "url": "2.0.0a15/api/index.html",
    "revision": "4c28f3b0c1e56841c98cfc0d54b5f3c8"
  },
  {
    "url": "2.0.0a15/api/log.html",
    "revision": "35669a961a5097dca0fdc395455fb49d"
  },
  {
    "url": "2.0.0a15/api/matcher.html",
    "revision": "602ded370b7780619cd6fdf45e477151"
  },
  {
    "url": "2.0.0a15/api/message.html",
    "revision": "f6f2d777464e753b302b0dee12ed2417"
  },
  {
    "url": "2.0.0a15/api/nonebot.html",
    "revision": "835f4970273d4f9e02b24b7ced10574d"
  },
  {
    "url": "2.0.0a15/api/permission.html",
    "revision": "f07c20a76ac29adc8b750fa4a6e4556c"
  },
  {
    "url": "2.0.0a15/api/plugin.html",
    "revision": "838426224e55a77999b9b6c1a9158634"
  },
  {
    "url": "2.0.0a15/api/rule.html",
    "revision": "cb235c7e0612911bcd50fd4e4ec3d336"
  },
  {
    "url": "2.0.0a15/api/typing.html",
    "revision": "8b0fe3aa230e9038948939db92ffea8d"
  },
  {
    "url": "2.0.0a15/api/utils.html",
    "revision": "3af6f5396c1372ecf71b8aaea6973603"
  },
  {
    "url": "2.0.0a15/guide/basic-configuration.html",
    "revision": "5b142e9eaa07ae2fd3a80eed48935bd3"
  },
  {
    "url": "2.0.0a15/guide/cqhttp-guide.html",
    "revision": "5b9b71c0c601a539f537ef3ed050749d"
  },
  {
    "url": "2.0.0a15/guide/creating-a-handler.html",
    "revision": "a3d8c53fe7c6427af669b1033ffe553e"
  },
  {
    "url": "2.0.0a15/guide/creating-a-matcher.html",
    "revision": "f2e3742356a4dcb8e8c6a291723801b5"
  },
  {
    "url": "2.0.0a15/guide/creating-a-plugin.html",
    "revision": "f81f476187ffb6ec88d9498fa7766b5a"
  },
  {
    "url": "2.0.0a15/guide/creating-a-project.html",
    "revision": "fd4d58efb4358a99edc31a5185bdf482"
  },
  {
    "url": "2.0.0a15/guide/ding-guide.html",
    "revision": "955ef03754f811fed055c6b517b9ebc2"
  },
  {
    "url": "2.0.0a15/guide/end-or-start.html",
    "revision": "c2fd21ad18430e881160da1174d8dfff"
  },
  {
    "url": "2.0.0a15/guide/feishu-guide.html",
    "revision": "d261da5b4da0d329b124f25c13ed940e"
  },
  {
    "url": "2.0.0a15/guide/getting-started.html",
    "revision": "f21ccc3218f29477143580a42a770ec7"
  },
  {
    "url": "2.0.0a15/guide/index.html",
    "revision": "bf812c1f1445be3959e1b12e94a36ec4"
  },
  {
    "url": "2.0.0a15/guide/installation.html",
    "revision": "df170513dab3cca2bf3789219e6662f8"
  },
  {
    "url": "2.0.0a15/guide/loading-a-plugin.html",
    "revision": "8f57a713baab06194b6622c203b21a48"
  },
  {
    "url": "2.0.0a15/guide/mirai-guide.html",
    "revision": "8cfba4789e0c1cba2f77330c350ba7ec"
  },
  {
    "url": "2.0.0a15/index.html",
    "revision": "52d5c4e39dffbe000a6bfdcc0b5d71b2"
  },
  {
    "url": "404.html",
    "revision": "18cf27db590759cc3c092cf946645e78"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "ff79fe759105b739c1d200c1b6ea208d"
  },
  {
    "url": "advanced/index.html",
    "revision": "a5bb320b84c64ed4bd5d428ef0f46fb8"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "08dec354f7a027bc76f9980ba4bb06f8"
  },
  {
    "url": "advanced/permission.html",
    "revision": "130a030a97c56d45c401bb85150c2992"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "a5d4958015b7de69a2f32d92af5459a7"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "dae3dfc97042bdad1b4ce4a4b0134820"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "ed3f928e9180db33090a71e478ea9b9c"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "6a48061f74167211f9e75375a0991a11"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "27e695227409e0e7be05ec427e15cc89"
  },
  {
    "url": "api/adapters/feishu.html",
    "revision": "7203149f85f3c3e1dd7c568eac5b480e"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "e50d25ca752b565ba2e7aa42c69ee62f"
  },
  {
    "url": "api/adapters/mirai.html",
    "revision": "94eb9df6fc8a6fe30255af7fb6762f48"
  },
  {
    "url": "api/config.html",
    "revision": "1876d4fee5027f03926293bb559bbb73"
  },
  {
    "url": "api/drivers/aiohttp.html",
    "revision": "46ba48eaa493a1c54bbaea58754d5467"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "53f0c00b669f65970933a70ecbdb1f44"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "c2195f4a30be1abdb706f1cc702460f1"
  },
  {
    "url": "api/drivers/quart.html",
    "revision": "7720ff8f4edef184ca20161b06fdefd2"
  },
  {
    "url": "api/exception.html",
    "revision": "ab6afdbbef308c5754aedf66a1fbbe74"
  },
  {
    "url": "api/handler.html",
    "revision": "32cb70c4c9ce2826d0b2db8c7f30b4e1"
  },
  {
    "url": "api/index.html",
    "revision": "f44433d615d57424fff860c4c13d2282"
  },
  {
    "url": "api/log.html",
    "revision": "7b13b3ff8bb3437f8b68fcc4ea8639cc"
  },
  {
    "url": "api/matcher.html",
    "revision": "504cbc6a8643fa50e83a00deee617f1c"
  },
  {
    "url": "api/message.html",
    "revision": "657bc09a9cc5cd7516e918dcb17b43ba"
  },
  {
    "url": "api/nonebot.html",
    "revision": "e7ab163c2b423bff2af962c4654ae84d"
  },
  {
    "url": "api/permission.html",
    "revision": "c3530b325f1268020d39621de47745ca"
  },
  {
    "url": "api/plugin.html",
    "revision": "208c112c70b83d74d21c0485fc5ad544"
  },
  {
    "url": "api/rule.html",
    "revision": "a2e5b1b98022a751f1a8e6045fefffe8"
  },
  {
    "url": "api/typing.html",
    "revision": "f68ff7be7c825882329cea311af9c499"
  },
  {
    "url": "api/utils.html",
    "revision": "362968eb8fd22b4c6632713b20482fd0"
  },
  {
    "url": "assets/css/0.styles.92d96405.css",
    "revision": "5a3d1d298d6ccc32ea2699b83042f28b"
  },
  {
    "url": "assets/img/Handle-Event.1e964e39.png",
    "revision": "1e964e39a1e302bc36072da2ffe9f509"
  },
  {
    "url": "assets/img/jiaqian.9b09040e.png",
    "revision": "9b09040ed4e5e35000247aa00e6dceac"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/img/webhook.479198ed.png",
    "revision": "479198ed677c8ba4bbdf72d0a60497c9"
  },
  {
    "url": "assets/js/1.b21fc040.js",
    "revision": "3d5117e32c838f7f5716094927838374"
  },
  {
    "url": "assets/js/10.9d20304b.js",
    "revision": "f2d33dd5c140fb5e73f5abf7448239c3"
  },
  {
    "url": "assets/js/100.11366615.js",
    "revision": "c9e51dbed6584a5bb21dc13aa3e0eec5"
  },
  {
    "url": "assets/js/101.dd7d03f8.js",
    "revision": "ee496f1846587eb1678830e25dbd761f"
  },
  {
    "url": "assets/js/102.392a2aae.js",
    "revision": "f3d5ceb94435afb22d47b0c606925985"
  },
  {
    "url": "assets/js/103.47f8b659.js",
    "revision": "bcb9d3514602487d61fa0d39076d569d"
  },
  {
    "url": "assets/js/104.a1415d21.js",
    "revision": "59eab35b5197dcac95efea6492d4f064"
  },
  {
    "url": "assets/js/105.77264bd3.js",
    "revision": "e3c07d367b2d4ad88cf1ad7e8c50d1bd"
  },
  {
    "url": "assets/js/106.213f3b94.js",
    "revision": "b5d2f113365f6f5ead1591242fb02c2f"
  },
  {
    "url": "assets/js/107.a4f2ac83.js",
    "revision": "e255d54c07b20833dc5c8b102271925c"
  },
  {
    "url": "assets/js/108.964d0813.js",
    "revision": "17c531a5fe26b31c8315cc37792692d3"
  },
  {
    "url": "assets/js/109.705b7b8c.js",
    "revision": "2670957b47a55f1f7926ffcfe79146d8"
  },
  {
    "url": "assets/js/11.caec9e04.js",
    "revision": "6f87ff7fc8dab8cb6a0b796f0653951d"
  },
  {
    "url": "assets/js/110.a21558a0.js",
    "revision": "c096a686d57efb9b7a15ea336adae8ba"
  },
  {
    "url": "assets/js/111.201fc390.js",
    "revision": "3aad2e97de4f7b7afad96ace2e35c749"
  },
  {
    "url": "assets/js/112.4a2478f7.js",
    "revision": "7a0af70cdc25a8953fda87c9bea73b9a"
  },
  {
    "url": "assets/js/113.2e3739ff.js",
    "revision": "aa983e55484ee9d45da8f7935f69717c"
  },
  {
    "url": "assets/js/114.b3be7899.js",
    "revision": "c9d40056122b8f2bf8db128df05aa58f"
  },
  {
    "url": "assets/js/115.1f530f36.js",
    "revision": "b7d22f38572d4fe903ba0ae1efbb405a"
  },
  {
    "url": "assets/js/116.79613e2c.js",
    "revision": "5a7deffeb9fde667b7d0cd022a89c83e"
  },
  {
    "url": "assets/js/117.049907eb.js",
    "revision": "f79b4995ea9ffff622a11b9b9d0b09d3"
  },
  {
    "url": "assets/js/118.4dbb2b0c.js",
    "revision": "611fa6a9066f62683dcd390f11a37f34"
  },
  {
    "url": "assets/js/119.06fcf124.js",
    "revision": "f6024560ba4631d11238616f9fc485e9"
  },
  {
    "url": "assets/js/12.3eae06d0.js",
    "revision": "26d11a4dc9e3b7aceb45087ab36e8b21"
  },
  {
    "url": "assets/js/120.3d6c5d61.js",
    "revision": "d191483ce111a8b13cc0c7bb9e3867a7"
  },
  {
    "url": "assets/js/121.04883476.js",
    "revision": "a4df34bfbe38ff4562a240bc8cb8e845"
  },
  {
    "url": "assets/js/122.9a5d2f89.js",
    "revision": "6cf34914b8002b0ffc101fe47b56014c"
  },
  {
    "url": "assets/js/123.0e0fb84b.js",
    "revision": "7b1b9e21310e1e511b4187ce448b316c"
  },
  {
    "url": "assets/js/124.94ef90af.js",
    "revision": "2c0d34132cc9343721288608f86cbb17"
  },
  {
    "url": "assets/js/125.d8ec14ee.js",
    "revision": "1a830b9f9f14e84ba347f56fd242fb9e"
  },
  {
    "url": "assets/js/126.aeab2bca.js",
    "revision": "d7fbc53894c0bbfa346db00de5fdb2a9"
  },
  {
    "url": "assets/js/127.5c93fa63.js",
    "revision": "2f19c79f4fdd0fdcc79815f744192520"
  },
  {
    "url": "assets/js/128.78a4b712.js",
    "revision": "24ecdfc16388f2f27779474e090f3667"
  },
  {
    "url": "assets/js/129.f3d1ffe3.js",
    "revision": "33538e09556aef2e0aa2d738f9dbe8c1"
  },
  {
    "url": "assets/js/13.aab176fa.js",
    "revision": "6ec96de745ee367eae2dec6073a0be27"
  },
  {
    "url": "assets/js/130.5b653c56.js",
    "revision": "abf4f48f17b253f8468d47dde9e6ed53"
  },
  {
    "url": "assets/js/131.d80554ca.js",
    "revision": "dc2ef3cf848e0686ad14805acbaed0bc"
  },
  {
    "url": "assets/js/132.97f88d7d.js",
    "revision": "9aa266da3a7c9d3a89bbab72e8ad5adc"
  },
  {
    "url": "assets/js/133.62ec43e5.js",
    "revision": "ae4bb5089f3b3824161552a08d06d8b1"
  },
  {
    "url": "assets/js/134.b13687b1.js",
    "revision": "11c436bc9c9a666148cf0ce47d420781"
  },
  {
    "url": "assets/js/135.624f1971.js",
    "revision": "1cd7a24f99bc4e92be69fe00cfee21ff"
  },
  {
    "url": "assets/js/136.0b0c2d76.js",
    "revision": "9e69131b6bfbc70b53df10106ef3e114"
  },
  {
    "url": "assets/js/137.1298330b.js",
    "revision": "04caa4a7f932c81c9ad504225e0965de"
  },
  {
    "url": "assets/js/138.0a1e2fbe.js",
    "revision": "eaed48b6c35b07535d6ab48f14325525"
  },
  {
    "url": "assets/js/139.6680ceb0.js",
    "revision": "45ef63e75e63b9960735d80ea1abd9b6"
  },
  {
    "url": "assets/js/14.94085abf.js",
    "revision": "ddd747c0178a81602fe9702ddc2f561a"
  },
  {
    "url": "assets/js/140.10b72b9f.js",
    "revision": "e508943c2a2ed2baab3260ef1e0d1cdd"
  },
  {
    "url": "assets/js/141.69835e59.js",
    "revision": "79085052f110b775a82926c92ec578b4"
  },
  {
    "url": "assets/js/142.fdf4c805.js",
    "revision": "0a97462e1e31634d8e60198e4a44cffd"
  },
  {
    "url": "assets/js/143.2ae9f37c.js",
    "revision": "eff6a2eb7c99a71c82cb39fe150b7da6"
  },
  {
    "url": "assets/js/144.98f299f5.js",
    "revision": "32161c50f4040a0731a1b8379a28de9f"
  },
  {
    "url": "assets/js/145.b5fffef3.js",
    "revision": "52e3eef3f1e7ced49f2d5e12938fd4cf"
  },
  {
    "url": "assets/js/146.76ec6516.js",
    "revision": "9943526e4b3c645c94fa14ad8c0c7bc3"
  },
  {
    "url": "assets/js/147.5064f178.js",
    "revision": "37cae508ce5811ad139163a6fb8cbdd8"
  },
  {
    "url": "assets/js/148.3693b38d.js",
    "revision": "b85cf1b643fce1862c8202fbc16ea22a"
  },
  {
    "url": "assets/js/149.fee07451.js",
    "revision": "02119fe2df556bcd0691e3badbc2d527"
  },
  {
    "url": "assets/js/15.e7f73ea5.js",
    "revision": "dbb9e6dfa0f8dbcd72e6f7e39fd80ea0"
  },
  {
    "url": "assets/js/150.802a93fd.js",
    "revision": "0b1176d15552bbd1b19d520682ff101d"
  },
  {
    "url": "assets/js/151.5c03c72d.js",
    "revision": "f72b0992d284078d3e64fe4ad9a30a03"
  },
  {
    "url": "assets/js/152.03a913bc.js",
    "revision": "514a6b73f4630e33a22b853bdf0b1726"
  },
  {
    "url": "assets/js/153.1c407b0f.js",
    "revision": "bfe96d3d1a87e850a449a08765eb9e60"
  },
  {
    "url": "assets/js/154.2a8951e0.js",
    "revision": "bdf7deb0e0ca38dcfddab4b9666b6c51"
  },
  {
    "url": "assets/js/155.ee95a6ac.js",
    "revision": "c259cdf25eb0cfdcb00b518aa00120ed"
  },
  {
    "url": "assets/js/156.e5cfb6f4.js",
    "revision": "bb2242225c24744160eed94c30874c55"
  },
  {
    "url": "assets/js/157.86c1f6e0.js",
    "revision": "6605182c3da351fb468208ec44ec1d93"
  },
  {
    "url": "assets/js/158.d564ffa9.js",
    "revision": "a17e9450d780a0744e6130bd37d9703e"
  },
  {
    "url": "assets/js/159.4db7f34a.js",
    "revision": "4c9f797fb45397ad3ce68b127f7ec7c0"
  },
  {
    "url": "assets/js/16.06fecefd.js",
    "revision": "fd14780b28732adeb7241ce1dc8cc810"
  },
  {
    "url": "assets/js/160.ca9b01a7.js",
    "revision": "23dc2f85bed8afc4d41a20f3a3dc2c45"
  },
  {
    "url": "assets/js/161.9d9efeec.js",
    "revision": "b85d7ed14954efbc77cf8dde3ed88f93"
  },
  {
    "url": "assets/js/162.c8652c3e.js",
    "revision": "5d9ca08e3c34389e742344a492b78935"
  },
  {
    "url": "assets/js/163.413dffc3.js",
    "revision": "cdbdfed2519815222180dab018e7df77"
  },
  {
    "url": "assets/js/164.0b6db967.js",
    "revision": "a1d385c33d689ab6472612e4cb034538"
  },
  {
    "url": "assets/js/165.7b714f80.js",
    "revision": "ea07e7111b1f361372699cdb9ff6bf9b"
  },
  {
    "url": "assets/js/166.d3754cbc.js",
    "revision": "c32cb7201298573f3a8603b96494c81d"
  },
  {
    "url": "assets/js/167.52f3f39c.js",
    "revision": "cb051cb723f0b698fcc449f11ff3d710"
  },
  {
    "url": "assets/js/168.6cf29fdf.js",
    "revision": "f0a7f0aad0e60d1c9b98aeb9f901886f"
  },
  {
    "url": "assets/js/169.39531875.js",
    "revision": "1d928068b0d0834ec758255d74a3a1a7"
  },
  {
    "url": "assets/js/17.b1c4e7d8.js",
    "revision": "f92fb8692f0564d0011f68c4c5ff0716"
  },
  {
    "url": "assets/js/170.224b0928.js",
    "revision": "b0c85479affccdfff67380b50fca9dad"
  },
  {
    "url": "assets/js/171.5c627637.js",
    "revision": "41ab7925e96ad2baebce6aafbc2a2054"
  },
  {
    "url": "assets/js/172.eab6e0df.js",
    "revision": "478ddcc38017b6ab326fc4b81106f669"
  },
  {
    "url": "assets/js/173.bab3426b.js",
    "revision": "19c1bcc39aed47440ad75eaca4efe90f"
  },
  {
    "url": "assets/js/174.02ab25a0.js",
    "revision": "858fe5693461dedbc9385e7d8e8c3806"
  },
  {
    "url": "assets/js/175.e895e715.js",
    "revision": "bd2a3037c15a6a8e2e20f8621fd6b019"
  },
  {
    "url": "assets/js/176.cf95e56d.js",
    "revision": "17e03a324089aba637b2669a0e88a5b5"
  },
  {
    "url": "assets/js/177.94de4a90.js",
    "revision": "ce137eb5966fe5de023992b96f63533e"
  },
  {
    "url": "assets/js/178.215ba1c0.js",
    "revision": "f02cd419cf02491f5f3a6abfcbccd3f2"
  },
  {
    "url": "assets/js/179.380d9d27.js",
    "revision": "27c57a78e16a30e4335a7db79e8b10fd"
  },
  {
    "url": "assets/js/18.eca99d58.js",
    "revision": "373f0006b05b741196fb92914ec83be5"
  },
  {
    "url": "assets/js/180.9302a87f.js",
    "revision": "85076f0437375083e05d037123f2df8b"
  },
  {
    "url": "assets/js/181.d6909d2b.js",
    "revision": "958d35107f88c18cd5e90ceffae1442f"
  },
  {
    "url": "assets/js/182.4c62b7d8.js",
    "revision": "127e2dba3bfcf66fb0f9265366b73c53"
  },
  {
    "url": "assets/js/183.701dd048.js",
    "revision": "7741435ee62053c147cc4b0e29e26519"
  },
  {
    "url": "assets/js/184.5e0dfc87.js",
    "revision": "93dc407fe93181f8f1bc8ff238b070db"
  },
  {
    "url": "assets/js/185.42ec2a61.js",
    "revision": "9476d6b4666f666ea1664d7034c58a40"
  },
  {
    "url": "assets/js/186.c39e8e39.js",
    "revision": "8e8b4d488127cab713a3aff4b4132256"
  },
  {
    "url": "assets/js/187.68e80dbd.js",
    "revision": "483f172132e4dbceb27bcb42290f8445"
  },
  {
    "url": "assets/js/188.cd860928.js",
    "revision": "961d23e81d9b7b53051bb84c89a549bf"
  },
  {
    "url": "assets/js/189.e9d18a35.js",
    "revision": "eb639008722856c7078d99a04fd3bc05"
  },
  {
    "url": "assets/js/19.c307a8aa.js",
    "revision": "047b2d7e110411d00b2e7bbc6760458a"
  },
  {
    "url": "assets/js/20.66877632.js",
    "revision": "03381439f9e52f27b90ef17e55f570bb"
  },
  {
    "url": "assets/js/21.6c7517b8.js",
    "revision": "421b70d8d4bbaca92581f4b3cdc7efb3"
  },
  {
    "url": "assets/js/22.b749d315.js",
    "revision": "6a55adba7daf6b44cd15d680d5a9e3c4"
  },
  {
    "url": "assets/js/23.8a3554d2.js",
    "revision": "147ac965aa3b804c56065084c9e236f2"
  },
  {
    "url": "assets/js/24.a4a63ab0.js",
    "revision": "9aa6209e7f90795055a56f17e2340aad"
  },
  {
    "url": "assets/js/25.60d16bc3.js",
    "revision": "b76494f1dbd8b69ed790d29bac52f994"
  },
  {
    "url": "assets/js/26.87356090.js",
    "revision": "ea10fe861e234dc3bf136c0b391716ae"
  },
  {
    "url": "assets/js/27.963b78b9.js",
    "revision": "361c527fea6b29bb033a89f60b764a8c"
  },
  {
    "url": "assets/js/28.54615028.js",
    "revision": "499febf6ab7b7e42c392394b65053a78"
  },
  {
    "url": "assets/js/29.4941113c.js",
    "revision": "037ffe31c7dfaacb93d9a5527b7eb0c8"
  },
  {
    "url": "assets/js/30.703d301d.js",
    "revision": "8dcd54f384b57cc99e5ec3bd311e01c0"
  },
  {
    "url": "assets/js/31.a17825c8.js",
    "revision": "f8561158858de0e7f3610c3f15908afe"
  },
  {
    "url": "assets/js/32.86bff8f2.js",
    "revision": "3e3ed7b1fa591d9769c16d902d644c38"
  },
  {
    "url": "assets/js/33.470f7089.js",
    "revision": "a638a2995da9be6e7d69dc9d04275bab"
  },
  {
    "url": "assets/js/34.94b52620.js",
    "revision": "845981c9b6e3dbfc7a2ea728d19f4602"
  },
  {
    "url": "assets/js/35.4bccd8ae.js",
    "revision": "2d917fca0841dc05baef43381f64ab6f"
  },
  {
    "url": "assets/js/36.897722dc.js",
    "revision": "6fdda011353138434629b3904a176c60"
  },
  {
    "url": "assets/js/37.c1d3b441.js",
    "revision": "73fb7e68b62cb0bee7fcf0ad3d6c280a"
  },
  {
    "url": "assets/js/38.5931721e.js",
    "revision": "1873c8e55dbed1b36a151265eb2aad29"
  },
  {
    "url": "assets/js/39.0e6f6087.js",
    "revision": "c4c5806ae9d4c0ed6aab2f0b2550776c"
  },
  {
    "url": "assets/js/4.da5c5406.js",
    "revision": "cd12130ca24c93074429c66ee311eb18"
  },
  {
    "url": "assets/js/40.992bcf58.js",
    "revision": "c4acf597691fede8612dbfac46c51b11"
  },
  {
    "url": "assets/js/41.231a9c17.js",
    "revision": "21fa5fd39e903f82e42006e79b671f55"
  },
  {
    "url": "assets/js/42.8855a8c3.js",
    "revision": "e551d170b70d931d45deae76177eb028"
  },
  {
    "url": "assets/js/43.1259fd2e.js",
    "revision": "5d1be2fefc37298f594127a3cb56d0af"
  },
  {
    "url": "assets/js/44.9c810b88.js",
    "revision": "899b8d7a510655b0453ca8d5fb79345c"
  },
  {
    "url": "assets/js/45.9480d583.js",
    "revision": "a67f7518f80741246fc49996bba39975"
  },
  {
    "url": "assets/js/46.54f69e91.js",
    "revision": "707d4ac930e0c6bbad6718fa359bd78a"
  },
  {
    "url": "assets/js/47.3b1c74aa.js",
    "revision": "74165ebc0c66751220760a1aed5833a6"
  },
  {
    "url": "assets/js/48.30b0ad1f.js",
    "revision": "d15a09bd6bcb35ec025d40509f37b65f"
  },
  {
    "url": "assets/js/49.55e03b6b.js",
    "revision": "271b04accae6cf39ce6cab45d6b3f8ca"
  },
  {
    "url": "assets/js/5.12a0b895.js",
    "revision": "1908c816b77940b781c1c789531d7631"
  },
  {
    "url": "assets/js/50.c12cbcfa.js",
    "revision": "cb5edeb6a4b18d92749bd8ffcb973307"
  },
  {
    "url": "assets/js/51.691f2e1d.js",
    "revision": "ee2f6c97c783ba260ac54d5a99ea48f2"
  },
  {
    "url": "assets/js/52.ce4df92d.js",
    "revision": "bb52fbe5c24f63d59f13ea13d9b7710d"
  },
  {
    "url": "assets/js/53.3db147e1.js",
    "revision": "f31292055b1e6babc90cea2f014fe056"
  },
  {
    "url": "assets/js/54.c3d5719d.js",
    "revision": "a9de8c4be1a0fbd89e5a49506968d93b"
  },
  {
    "url": "assets/js/55.97587eb7.js",
    "revision": "9b91d8ec7a9a153342823921ee434977"
  },
  {
    "url": "assets/js/56.28d7b844.js",
    "revision": "2e12b7a0306f46701064362eff0dad73"
  },
  {
    "url": "assets/js/57.6d196621.js",
    "revision": "26924835059daee9f81923cbf359df71"
  },
  {
    "url": "assets/js/58.d456d4d9.js",
    "revision": "bd8ba9c2fe8a6e6d5585fe92eeae03ca"
  },
  {
    "url": "assets/js/59.02f4c2e9.js",
    "revision": "1ad0ef945ec397193541ad4cc059c1c7"
  },
  {
    "url": "assets/js/6.0dba5119.js",
    "revision": "dd8852a5c04c91f0a926f32e3d56be01"
  },
  {
    "url": "assets/js/60.ce8b2cfe.js",
    "revision": "af7d154279651622f514fc6b6fbc3aa6"
  },
  {
    "url": "assets/js/61.00b847e1.js",
    "revision": "652ad6e1c6706dbbb56f785a7490e77a"
  },
  {
    "url": "assets/js/62.493ccae2.js",
    "revision": "4d2d2b544eba1dae7c484a64cc958eee"
  },
  {
    "url": "assets/js/63.81843e46.js",
    "revision": "0515b62ba2d96197cc15712fa5c1b0a7"
  },
  {
    "url": "assets/js/64.9e720fba.js",
    "revision": "9ced15f1b4c699de1485a17a2143b3af"
  },
  {
    "url": "assets/js/65.26e86a7d.js",
    "revision": "2749cbf33655e6a61b6562cfe79b3613"
  },
  {
    "url": "assets/js/66.e8d5dcb1.js",
    "revision": "12c60abd7db0444217e6cc91ced4c12e"
  },
  {
    "url": "assets/js/67.46d67cb6.js",
    "revision": "ad31fc226baf0711eba0e8e400f32223"
  },
  {
    "url": "assets/js/68.63423cbb.js",
    "revision": "699c65c71668ed628bac1a235ea040a8"
  },
  {
    "url": "assets/js/69.a1d9482d.js",
    "revision": "733ee0e7670436f0bdf47e75a9cfaa6c"
  },
  {
    "url": "assets/js/7.8cca6999.js",
    "revision": "3a99233455e91777eb3ec14a8cdeebf9"
  },
  {
    "url": "assets/js/70.e8f61167.js",
    "revision": "01442d7cb444d3c9dc0383403aa11fa1"
  },
  {
    "url": "assets/js/71.f1590cf9.js",
    "revision": "c3ce9cf82de6f63867733b0a6a3096c3"
  },
  {
    "url": "assets/js/72.afc497e5.js",
    "revision": "f57b87b5faa7946c0a58ef57227edfa1"
  },
  {
    "url": "assets/js/73.a2b129bc.js",
    "revision": "974db8a6d327f27146e309445afdbb15"
  },
  {
    "url": "assets/js/74.f3bc92be.js",
    "revision": "8dbd1b6a0d0cfa4b73a68dc43cbf3447"
  },
  {
    "url": "assets/js/75.be5dd8bf.js",
    "revision": "7241df9c24b07ad2da5b511b1ef653e1"
  },
  {
    "url": "assets/js/76.805f7ae6.js",
    "revision": "fedfedb73693501cd24ee4d83c6c34f0"
  },
  {
    "url": "assets/js/77.f04f43b4.js",
    "revision": "30d5cd10a5c33a06ddf49c176349a33c"
  },
  {
    "url": "assets/js/78.ce49dd07.js",
    "revision": "19ececfc263d67f2c3c20e58447c8232"
  },
  {
    "url": "assets/js/79.075d1572.js",
    "revision": "2c0961f71cafaadf798c417f2ca92d66"
  },
  {
    "url": "assets/js/8.521d7c7c.js",
    "revision": "4eb370dee7fec078b43d7bd777bad59b"
  },
  {
    "url": "assets/js/80.48f63145.js",
    "revision": "8d384e88494e81a1448b1fa6c0b16594"
  },
  {
    "url": "assets/js/81.95357a54.js",
    "revision": "e3bb6f5c8b407a6df537d61ebb1c4d2c"
  },
  {
    "url": "assets/js/82.6e4a6a12.js",
    "revision": "7535d9622e3ef6aa23d542788c7a137f"
  },
  {
    "url": "assets/js/83.30d8621d.js",
    "revision": "b06da4d8c37c3ad711833822a0005b23"
  },
  {
    "url": "assets/js/84.b2d4dd90.js",
    "revision": "7065649d3ddd517dd72f91ff764025ec"
  },
  {
    "url": "assets/js/85.2da69266.js",
    "revision": "a07223fb3300d70227380cc24ff884b1"
  },
  {
    "url": "assets/js/86.26996224.js",
    "revision": "60a3aab4ecc87acdfbb62c337b916f2e"
  },
  {
    "url": "assets/js/87.8b3600f4.js",
    "revision": "1c366e84900dff5e9addeb56c5f0d0be"
  },
  {
    "url": "assets/js/88.5424156e.js",
    "revision": "994db63401279bbe1e8d1892b4a2665d"
  },
  {
    "url": "assets/js/89.e5f48621.js",
    "revision": "886b26c87b2ba7633c9b75811e1a52a2"
  },
  {
    "url": "assets/js/9.18b9f60a.js",
    "revision": "b0267141e6d0e1aa4937b44cdd28891e"
  },
  {
    "url": "assets/js/90.d9688c26.js",
    "revision": "d50e462261ec8503317b637d158faf97"
  },
  {
    "url": "assets/js/91.796cc0f0.js",
    "revision": "b81b086a24f4201804510b38f88f31af"
  },
  {
    "url": "assets/js/92.7e3633e3.js",
    "revision": "8166b94b6072e5820d68c986c93d2085"
  },
  {
    "url": "assets/js/93.23dff9df.js",
    "revision": "ec1e446737246c5709c6a37b7a9c0500"
  },
  {
    "url": "assets/js/94.1bdc4135.js",
    "revision": "0d6cf9d8f8017725353dd9337a7b0bbf"
  },
  {
    "url": "assets/js/95.4e5f15a0.js",
    "revision": "f5ca9258e7834986f4301428f8481c14"
  },
  {
    "url": "assets/js/96.f9503c4e.js",
    "revision": "e0cb5b3f5663152093682c36d5940dfa"
  },
  {
    "url": "assets/js/97.f23b810a.js",
    "revision": "d473e056b1c42916803b12174bf6e602"
  },
  {
    "url": "assets/js/98.7af0baa8.js",
    "revision": "912b5da5614a829c0c389d68672f7dcb"
  },
  {
    "url": "assets/js/99.db1da0a9.js",
    "revision": "a5887742287e5e3aea3ae807134451b4"
  },
  {
    "url": "assets/js/app.8d72956c.js",
    "revision": "d4ae12663226e08850e52537f2d2c1d4"
  },
  {
    "url": "assets/js/vendors~docsearch.d31fbf91.js",
    "revision": "a0550a200b8ca78444504bfad98a2bc4"
  },
  {
    "url": "changelog.html",
    "revision": "4a36b59af22495d7c9c023aeaf2a3bd0"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "415ce25970e53d6240aad676bc22e931"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "4ff547c872a8a38a54387494bd6b65c2"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "1cd6ab29b0877ab87c85992fefdef360"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "cb09dbc62ec1672f40b493b373947cdd"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "c55097a9dca171d7f07c3fb22a6c6db1"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "d65056dbcd8574dfb50a69a08b0b2260"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "7e1079dcc2f9d735412fb8d6d81efe79"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "24dc507b9b39ac4f33bcfa6bacd2be68"
  },
  {
    "url": "guide/feishu-guide.html",
    "revision": "57d08618bde2b66e661245992770aa90"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "4acd60fa3d598ba2529afaae56c7b4e5"
  },
  {
    "url": "guide/index.html",
    "revision": "2f535b8c3fd1e1c668aebb6ce9ca0b6c"
  },
  {
    "url": "guide/installation.html",
    "revision": "1b4a3b1e85145ba43db53bd28f2c6e11"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "870f8db66a391707c01350ffa2b00de5"
  },
  {
    "url": "guide/mirai-guide.html",
    "revision": "0ef2280bd087d2516d79ba67015c3a53"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "fbc4df64fd6c188ee0999dfd3c380b4e"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "b5796d4a8bedd8a3f315768c9924f95b"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "f29b87abc904b04dd1abdc15e21ade4e"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "7c4b6c44030e9c813ebf20fc34eddcd0"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "6d85d366ef46661dccc664e96ced37d8"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "01799fbde0c0b5419a625d62482bb356"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "17805938aeeec44a12581740d65c8431"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "799562e0207571cef015aaf9c7264509"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "01e88f0edaeaa3b3f7d4031673d5eb7f"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "9f6577def4d92780b6e3fff0884088a1"
  },
  {
    "url": "next/api/adapters/feishu.html",
    "revision": "3e5c3cd98cf59416645acff82435d0c6"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "7f34b68331158d6795784ce2778c0561"
  },
  {
    "url": "next/api/adapters/mirai.html",
    "revision": "4a373fdc654516aa4e8a2d58daf8c219"
  },
  {
    "url": "next/api/config.html",
    "revision": "23c6f4772d3a20db5989caf69059372e"
  },
  {
    "url": "next/api/drivers/aiohttp.html",
    "revision": "5949b8986abcb9b2c431994fdcce3a87"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "175200f0f189134a3bc12b4e91e0630a"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "ed4c10b65884d9564581579ac1447cc9"
  },
  {
    "url": "next/api/drivers/quart.html",
    "revision": "f50cf5d80b8f12d9dfeff0cac99aa750"
  },
  {
    "url": "next/api/exception.html",
    "revision": "42233ed443657b45db41fea07db2618f"
  },
  {
    "url": "next/api/handler.html",
    "revision": "71f0123ada9864cb14ef60b929069b1f"
  },
  {
    "url": "next/api/index.html",
    "revision": "9447727a791ab6e401022808cdc03b3a"
  },
  {
    "url": "next/api/log.html",
    "revision": "65e01c21e0e45312d6c319c42581e7ec"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "fadeaba701fa8d299fd82ddbb497e632"
  },
  {
    "url": "next/api/message.html",
    "revision": "065be09b49ddadc82850041e5b457d89"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "513f2d955315c3c05bc330c1886a8b2f"
  },
  {
    "url": "next/api/permission.html",
    "revision": "0c9116bc49fd77a23381b0a4599da0a4"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "2a53e8d9a8e63d9961a030c80b3b5729"
  },
  {
    "url": "next/api/rule.html",
    "revision": "fea87a7241c01f97bffe51c3d6a6ef7e"
  },
  {
    "url": "next/api/typing.html",
    "revision": "02042e37726134be8b3f6910d2246311"
  },
  {
    "url": "next/api/utils.html",
    "revision": "154ba1cccb95f0ea9bff75c0641d3c80"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "f802fe278a766cd73b67592f2d62958a"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "6915bdb0b4717aecae58d7354db30440"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "0bd76a2365c6819f7c3bf5e37aab8da8"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "dde529fc632276987966efced40902cc"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "f7cd88ace016c538dcf37e1714321394"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "ff18babcfd0e005385b584c50192d38d"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "e39ef585c4813d9e551389b276c7b7ee"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "b4e664e9a2e7ed72a09c5dc53330d090"
  },
  {
    "url": "next/guide/feishu-guide.html",
    "revision": "7331995787c4a5ca5f21e40210f3769a"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "b2765e9fb0d9579097bb4140b00efe4f"
  },
  {
    "url": "next/guide/index.html",
    "revision": "a085ebccedbdd9c22effdeeff4831f4c"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "6db5530150b9cd3bdae3d2e106eba388"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "0ec52237028e01b39616ad56c42bc0c0"
  },
  {
    "url": "next/guide/mirai-guide.html",
    "revision": "6f12b4220712d6216899730e0fd76509"
  },
  {
    "url": "next/index.html",
    "revision": "125bdf5c1a3edf12e2dac692d4193f6a"
  },
  {
    "url": "store.html",
    "revision": "c202a5f3f82a60c519619cf07886d54d"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
