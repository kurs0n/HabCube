import framebuf

glass_icon_buffer = bytearray(480)
fb_glass = framebuf.FrameBuffer(glass_icon_buffer, 80, 48, framebuf.MONO_HLSB)

code_icon_buffer = bytearray(480)
fb_code = framebuf.FrameBuffer(code_icon_buffer, 80, 48, framebuf.MONO_HLSB)

sport_icon_buffer = bytearray(480)
fb_sport = framebuf.FrameBuffer(sport_icon_buffer, 80, 48, framebuf.MONO_HLSB)

lang_icon_buffer = bytearray(480)
fb_lang = framebuf.FrameBuffer(lang_icon_buffer, 80, 48, framebuf.MONO_HLSB)

glasses_icon_buffer = bytearray(480)
fb_glasses = framebuf.FrameBuffer(glasses_icon_buffer, 80, 48, framebuf.MONO_HLSB)

def configure_icons():
    configure_water_icon()
    configure_code_icon()
    configure_sport_icon()
    configure_language_icon()
    configure_glasses_icon()

def configure_water_icon():
    TOP_Y = 5
    BOT_Y = 42 
    TOP_W = 44    
    BOT_W = 24     
    WATER_LEVEL = 0.5  

    center_x = 40
    x1_top = center_x - (TOP_W // 2)
    x2_top = center_x + (TOP_W // 2)
    x1_bot = center_x - (BOT_W // 2)
    x2_bot = center_x + (BOT_W // 2)

    fb_glass.line(x1_top, TOP_Y, x1_bot, BOT_Y, 1)
    fb_glass.line(x2_top, TOP_Y, x2_bot, BOT_Y, 1)
    fb_glass.line(x1_bot, BOT_Y, x2_bot, BOT_Y, 1)

    water_height_px = int((BOT_Y - TOP_Y) * WATER_LEVEL)
    water_surface_y = BOT_Y - water_height_px

    for y in range(BOT_Y - 1, water_surface_y, -1):
        ratio = (BOT_Y - y) / (BOT_Y - TOP_Y)
        current_half_w = (BOT_W // 2) + int((TOP_W - BOT_W) // 2 * ratio)
        fb_glass.hline(center_x - current_half_w + 1, y, current_half_w * 2 - 2, 1)

    for x in range(center_x - int((TOP_W/2 + BOT_W/2)/2 * WATER_LEVEL) - 4, 
                   center_x + int((TOP_W/2 + BOT_W/2)/2 * WATER_LEVEL) + 4, 2):
        fb_glass.pixel(x, water_surface_y, 1)

def configure_code_icon():
    fb_code.rect(15, 8, 50, 32, 1)
    fb_code.line(15, 16, 65, 16, 1)
    fb_code.fill_rect(18, 12, 2, 2, 1)
    fb_code.fill_rect(22, 12, 2, 2, 1)
    fb_code.fill_rect(26, 12, 2, 2, 1)
    fb_code.text(">", 18, 20, 1)
    fb_code.hline(28, 23, 20, 1)
    fb_code.hline(28, 29, 15, 1)
    fb_code.hline(18, 35, 30, 1)

def configure_sport_icon():
    fb_sport.fill_rect(28, 22, 24, 4, 1)
    fb_sport.fill_rect(20, 14, 8, 20, 1)
    fb_sport.fill_rect(16, 16, 4, 16, 1)
    fb_sport.fill_rect(52, 14, 8, 20, 1)
    fb_sport.fill_rect(60, 16, 4, 16, 1)

def configure_language_icon():
    fb_lang.rect(15, 8, 32, 20, 1)
    fb_lang.line(15, 28, 20, 33, 1)
    fb_lang.line(20, 33, 25, 28, 1)
    fb_lang.hline(20, 15, 22, 1)
    fb_lang.hline(20, 21, 15, 1)
    
    fb_lang.fill_rect(38, 18, 34, 24, 0)
    fb_lang.rect(40, 20, 32, 20, 1)
    fb_lang.line(62, 40, 67, 45, 1)
    fb_lang.line(67, 45, 72, 40, 1)
    fb_lang.hline(45, 27, 22, 1)
    fb_lang.hline(45, 33, 15, 1)

def configure_glasses_icon():
    fb_glasses.rect(15, 18, 22, 14, 1)
    fb_glasses.rect(43, 18, 22, 14, 1)
    
    fb_glasses.hline(37, 22, 6, 1)
    
    fb_glasses.line(15, 18, 5, 12, 1)
    fb_glasses.line(65, 18, 75, 12, 1)
    
    fb_glasses.pixel(18, 21, 1)
    fb_glasses.pixel(46, 21, 1)
