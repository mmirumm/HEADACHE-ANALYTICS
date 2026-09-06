// Запускается внутри Figma как code.js локального плагина.
// Создаёт новый фрейм; существующий дизайн не изменяет.
const nodes = [{"kind": "rect", "name": "Header / Mark", "x": 96, "y": 44, "width": 42, "height": 42, "fill": "#45877C", "radius": 12, "stroke": null, "dash": false}, {"kind": "text", "name": "Header / Initial", "x": 107, "y": 47, "width": 28, "text": "M", "size": 26, "color": "#FFFFFF", "bold": true, "lineHeight": 36}, {"kind": "text", "name": "Header / Brand", "x": 152, "y": 44, "width": 200, "text": "MigreBot", "size": 27, "color": "#243B3B", "bold": true, "lineHeight": 38}, {"kind": "text", "name": "Header / Descriptor", "x": 1063, "y": 53, "width": 290, "text": "Ваш дневник головной боли", "size": 15, "color": "#687B79", "bold": false, "lineHeight": 21}, {"kind": "rect", "name": "Header / Divider", "x": 96, "y": 116, "width": 1248, "height": 1, "fill": "#DEE7E3", "radius": 0, "stroke": null, "dash": false}, {"kind": "rect", "name": "Intro / Eyebrow background", "x": 96, "y": 174, "width": 224, "height": 30, "fill": "#EAF3EF", "radius": 15, "stroke": null, "dash": false}, {"kind": "text", "name": "Intro / Eyebrow", "x": 111, "y": 180, "width": 204, "text": "РАЗБИРАЕМСЯ ВМЕСТЕ", "size": 12, "color": "#45877C", "bold": true, "lineHeight": 17}, {"kind": "text", "name": "Intro / Greeting", "x": 96, "y": 239, "width": 615, "text": "Добро пожаловать\nв MigreBot", "size": 58, "color": "#243B3B", "bold": true, "lineHeight": 67}, {"kind": "text", "name": "Intro / Description", "x": 96, "y": 410, "width": 590, "text": "Ваши записи о головной боли — в понятных графиках.\nЗагрузите дневник из бота и посмотрите, как часто\nвозникает боль и как меняются ваши оценки.", "size": 19, "color": "#687B79", "bold": false, "lineHeight": 30}, {"kind": "rect", "name": "Intro / Chip Дни с болью", "x": 96, "y": 540, "width": 144, "height": 38, "fill": "#F2F6F5", "radius": 19, "stroke": null, "dash": false}, {"kind": "text", "name": "Intro / Chip label Дни с болью", "x": 112, "y": 548, "width": 122, "text": "Дни с болью", "size": 14, "color": "#45877C", "bold": false, "lineHeight": 20}, {"kind": "rect", "name": "Intro / Chip Интенсивность", "x": 252, "y": 540, "width": 170, "height": 38, "fill": "#F2F6F5", "radius": 19, "stroke": null, "dash": false}, {"kind": "text", "name": "Intro / Chip label Интенсивность", "x": 268, "y": 548, "width": 148, "text": "Интенсивность", "size": 14, "color": "#45877C", "bold": false, "lineHeight": 20}, {"kind": "rect", "name": "Intro / Chip Динамика", "x": 434, "y": 540, "width": 122, "height": 38, "fill": "#F2F6F5", "radius": 19, "stroke": null, "dash": false}, {"kind": "text", "name": "Intro / Chip label Динамика", "x": 450, "y": 548, "width": 100, "text": "Динамика", "size": 14, "color": "#45877C", "bold": false, "lineHeight": 20}, {"kind": "text", "name": "Intro / Personal pace", "x": 96, "y": 614, "width": 600, "text": "Начните с одного файла. Остальное мы соберём на странице.", "size": 15, "color": "#687B79", "bold": false, "lineHeight": 21}, {"kind": "rect", "name": "Upload / Panel", "x": 790, "y": 174, "width": 554, "height": 485, "fill": "#FFFFFF", "radius": 24, "stroke": "#DEE7E3", "dash": false}, {"kind": "text", "name": "Upload / Heading", "x": 828, "y": 210, "width": 480, "text": "Начните со своего дневника", "size": 25, "color": "#243B3B", "bold": true, "lineHeight": 35}, {"kind": "text", "name": "Upload / Hint", "x": 828, "y": 257, "width": 466, "text": "Выберите CSV-файл, который вы выгрузили из бота.", "size": 16, "color": "#687B79", "bold": false, "lineHeight": 22}, {"kind": "rect", "name": "Upload / Dropzone", "x": 828, "y": 304, "width": 478, "height": 186, "fill": "#F5F9F7", "radius": 16, "stroke": "#9DBAB2", "dash": true}, {"kind": "text", "name": "Upload / File format", "x": 1040, "y": 326, "width": 80, "text": "CSV", "size": 20, "color": "#45877C", "bold": true, "lineHeight": 28}, {"kind": "text", "name": "Upload / Dropzone hint", "x": 892, "y": 369, "width": 380, "text": "Перетащите файл сюда или выберите его", "size": 16, "color": "#687B79", "bold": false, "lineHeight": 22}, {"kind": "rect", "name": "Upload / Button", "x": 969, "y": 412, "width": 194, "height": 48, "fill": "#45877C", "radius": 10, "stroke": null, "dash": false}, {"kind": "text", "name": "Upload / Button label", "x": 1002, "y": 423, "width": 156, "text": "Выбрать CSV", "size": 17, "color": "#FFFFFF", "bold": true, "lineHeight": 24}, {"kind": "rect", "name": "Upload / Demo checkbox", "x": 830, "y": 518, "width": 18, "height": 18, "fill": "#FFFFFF", "radius": 4, "stroke": "#9DBAB2", "dash": false}, {"kind": "text", "name": "Upload / Demo label", "x": 860, "y": 514, "width": 432, "text": "Посмотреть пример на вымышленных данных", "size": 16, "color": "#243B3B", "bold": false, "lineHeight": 22}, {"kind": "text", "name": "Upload / Format note", "x": 828, "y": 562, "width": 456, "text": "CSV до 5 МБ · Без регистрации", "size": 14, "color": "#687B79", "bold": false, "lineHeight": 20}, {"kind": "text", "name": "Upload / Privacy", "x": 828, "y": 593, "width": 456, "text": "При локальном запуске данные остаются на вашем Mac.", "size": 13, "color": "#687B79", "bold": false, "lineHeight": 18}, {"kind": "text", "name": "Steps / Heading", "x": 96, "y": 724, "width": 800, "text": "От записей — к понятной картине", "size": 27, "color": "#243B3B", "bold": true, "lineHeight": 38}, {"kind": "rect", "name": "Steps / Card 01", "x": 96, "y": 785, "width": 400, "height": 167, "fill": "#F2F6F5", "radius": 18, "stroke": null, "dash": false}, {"kind": "text", "name": "Steps / Number 01", "x": 120, "y": 805, "width": 50, "text": "01", "size": 15, "color": "#45877C", "bold": true, "lineHeight": 21}, {"kind": "text", "name": "Steps / Title 01", "x": 120, "y": 840, "width": 358, "text": "Выгрузите дневник", "size": 21, "color": "#243B3B", "bold": true, "lineHeight": 29}, {"kind": "text", "name": "Steps / Body 01", "x": 120, "y": 881, "width": 355, "text": "Сохраните историю записей\nиз Migrebot в формате CSV.", "size": 16, "color": "#687B79", "bold": false, "lineHeight": 24}, {"kind": "rect", "name": "Steps / Card 02", "x": 520, "y": 785, "width": 400, "height": 167, "fill": "#F2F6F5", "radius": 18, "stroke": null, "dash": false}, {"kind": "text", "name": "Steps / Number 02", "x": 544, "y": 805, "width": 50, "text": "02", "size": 15, "color": "#45877C", "bold": true, "lineHeight": 21}, {"kind": "text", "name": "Steps / Title 02", "x": 544, "y": 840, "width": 358, "text": "Загрузите файл", "size": 21, "color": "#243B3B", "bold": true, "lineHeight": 29}, {"kind": "text", "name": "Steps / Body 02", "x": 544, "y": 881, "width": 355, "text": "Выберите CSV на этой странице.\nДанные появятся автоматически.", "size": 16, "color": "#687B79", "bold": false, "lineHeight": 24}, {"kind": "rect", "name": "Steps / Card 03", "x": 944, "y": 785, "width": 400, "height": 167, "fill": "#F2F6F5", "radius": 18, "stroke": null, "dash": false}, {"kind": "text", "name": "Steps / Number 03", "x": 968, "y": 805, "width": 50, "text": "03", "size": 15, "color": "#45877C", "bold": true, "lineHeight": 21}, {"kind": "text", "name": "Steps / Title 03", "x": 968, "y": 840, "width": 358, "text": "Посмотрите динамику", "size": 21, "color": "#243B3B", "bold": true, "lineHeight": 29}, {"kind": "text", "name": "Steps / Body 03", "x": 968, "y": 881, "width": 355, "text": "Выберите период и изучите\nчастоту и интенсивность боли.", "size": 16, "color": "#687B79", "bold": false, "lineHeight": 24}, {"kind": "text", "name": "Footer / Note", "x": 96, "y": 987, "width": 1200, "text": "MigreBot · Наглядная история вашего самочувствия", "size": 14, "color": "#687B79", "bold": false, "lineHeight": 20}];
function rgb(hex) {
  return { r: parseInt(hex.slice(1, 3),16)/255,
           g: parseInt(hex.slice(3, 5),16)/255,
           b: parseInt(hex.slice(5, 7),16)/255 };
}
async function main() {
  await figma.loadFontAsync({family: "Arial", style: "Regular"});
  await figma.loadFontAsync({family: "Arial", style: "Bold"});
  const frame = figma.createFrame();
  frame.name = "MigreBot / Приветственная страница";
  frame.resize(1440, 1040);
  frame.fills = [{type:"SOLID", color:rgb("#FFFFFF")}];
  const bounds = figma.currentPage.children.filter(n => n.id !== frame.id);
  frame.x = bounds.length ? Math.max(...bounds.map(n => n.x+n.width))+100 : 0;
  frame.y = 0;
  for (const spec of nodes) {
    const node = spec.kind === "text" ? figma.createText() : figma.createRectangle();
    frame.appendChild(node);
    node.name = spec.name;
    node.x = spec.x;
    node.y = spec.y;
    if (spec.kind === "text") {
      node.fontName = {family:"Arial", style:spec.bold ? "Bold" : "Regular"};
      node.fontSize = spec.size;
      node.lineHeight = {value:spec.lineHeight, unit:"PIXELS"};
      node.characters = spec.text;
      node.fills = [{type:"SOLID", color:rgb(spec.color)}];
      node.resize(spec.width, spec.lineHeight);
      node.textAutoResize = "HEIGHT";
    } else {
      node.resize(spec.width, spec.height);
      node.cornerRadius = spec.radius;
      node.fills = [{type:"SOLID", color:rgb(spec.fill)}];
      if (spec.stroke) {
        node.strokes = [{type:"SOLID", color:rgb(spec.stroke)}];
        node.strokeWeight = 1;
        if (spec.dash) node.dashPattern = [6,5];
      }
    }
  }
  figma.currentPage.selection = [frame];
  figma.viewport.scrollAndZoomIntoView([frame]);
  figma.closePlugin("Макет MigreBot добавлен. Текст и блоки можно редактировать.");
}
main().catch(error => figma.closePlugin("Не удалось создать макет: " + error.message));
