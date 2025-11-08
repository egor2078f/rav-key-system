-- ========================================
-- RAV KEY SYSTEM - ROBLOX SCRIPT
-- ========================================

local KeySystem = {}

-- ⚙️ НАСТРОЙКИ - ИЗМЕНИ ЭТО!
local CONFIG = {
    BotURL = "https://t.me/YOUR_BOT_USERNAME", -- Замени на USERNAME своего бота!
    APIEndpoint = "https://web-production-785346.up.railway.app/", -- Замени на свой API URL!
    ScriptName = "RAV Script",
    Version = "1.0"
}

-- Сервисы
local TweenService = game:GetService("TweenService")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")

-- Создание UI
function KeySystem:CreateUI()
    -- Удаляем старое меню если есть
    if game.CoreGui:FindFirstChild("RAVKeySystem") then
        game.CoreGui:FindFirstChild("RAVKeySystem"):Destroy()
    end
    
    local ScreenGui = Instance.new("ScreenGui")
    local MainFrame = Instance.new("Frame")
    local UICorner = Instance.new("UICorner")
    local Title = Instance.new("TextLabel")
    local VersionLabel = Instance.new("TextLabel")
    local KeyBox = Instance.new("TextBox")
    local KeyBoxCorner = Instance.new("UICorner")
    local SubmitButton = Instance.new("TextButton")
    local SubmitCorner = Instance.new("UICorner")
    local GetKeyButton = Instance.new("TextButton")
    local GetKeyCorner = Instance.new("UICorner")
    local StatusLabel = Instance.new("TextLabel")
    local CloseButton = Instance.new("TextButton")
    local CloseCorner = Instance.new("UICorner")
    
    -- ScreenGui
    ScreenGui.Name = "RAVKeySystem"
    ScreenGui.Parent = game.CoreGui
    ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    ScreenGui.ResetOnSpawn = false
    
    -- MainFrame
    MainFrame.Name = "MainFrame"
    MainFrame.Parent = ScreenGui
    MainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
    MainFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 35)
    MainFrame.BorderSizePixel = 0
    MainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
    MainFrame.Size = UDim2.new(0, 0, 0, 0)
    MainFrame.ClipsDescendants = true
    
    -- Закругление
    UICorner.CornerRadius = UDim.new(0, 12)
    UICorner.Parent = MainFrame
    
    -- Заголовок
    Title.Name = "Title"
    Title.Parent = MainFrame
    Title.BackgroundTransparency = 1
    Title.Position = UDim2.new(0, 0, 0, 20)
    Title.Size = UDim2.new(1, 0, 0, 40)
    Title.Font = Enum.Font.GothamBold
    Title.Text = CONFIG.ScriptName .. " - Key System"
    Title.TextColor3 = Color3.fromRGB(255, 255, 255)
    Title.TextSize = 20
    Title.TextStrokeTransparency = 0.8
    
    -- Версия
    VersionLabel.Name = "VersionLabel"
    VersionLabel.Parent = MainFrame
    VersionLabel.BackgroundTransparency = 1
    VersionLabel.Position = UDim2.new(0, 0, 0, 55)
    VersionLabel.Size = UDim2.new(1, 0, 0, 20)
    VersionLabel.Font = Enum.Font.Gotham
    VersionLabel.Text = "Version " .. CONFIG.Version
    VersionLabel.TextColor3 = Color3.fromRGB(150, 150, 150)
    VersionLabel.TextSize = 12
    
    -- Поле ввода ключа
    KeyBox.Name = "KeyBox"
    KeyBox.Parent = MainFrame
    KeyBox.BackgroundColor3 = Color3.fromRGB(35, 35, 45)
    KeyBox.BorderSizePixel = 0
    KeyBox.Position = UDim2.new(0.5, 0, 0, 100)
    KeyBox.AnchorPoint = Vector2.new(0.5, 0)
    KeyBox.Size = UDim2.new(0, 340, 0, 45)
    KeyBox.Font = Enum.Font.Gotham
    KeyBox.PlaceholderText = "Введите ключ (RAV-1DAY-XXXX)"
    KeyBox.PlaceholderColor3 = Color3.fromRGB(100, 100, 100)
    KeyBox.Text = ""
    KeyBox.TextColor3 = Color3.fromRGB(255, 255, 255)
    KeyBox.TextSize = 14
    KeyBox.ClearTextOnFocus = false
    
    KeyBoxCorner.CornerRadius = UDim.new(0, 8)
    KeyBoxCorner.Parent = KeyBox
    
    -- Кнопка "Получить ключ"
    GetKeyButton.Name = "GetKeyButton"
    GetKeyButton.Parent = MainFrame
    GetKeyButton.BackgroundColor3 = Color3.fromRGB(52, 152, 219)
    GetKeyButton.BorderSizePixel = 0
    GetKeyButton.Position = UDim2.new(0.5, 0, 0, 160)
    GetKeyButton.AnchorPoint = Vector2.new(0.5, 0)
    GetKeyButton.Size = UDim2.new(0, 340, 0, 45)
    GetKeyButton.Font = Enum.Font.GothamBold
    GetKeyButton.Text = "🔑 Получить ключ"
    GetKeyButton.TextColor3 = Color3.fromRGB(255, 255, 255)
    GetKeyButton.TextSize = 15
    GetKeyButton.AutoButtonColor = false
    
    GetKeyCorner.CornerRadius = UDim.new(0, 8)
    GetKeyCorner.Parent = GetKeyButton
    
    -- Кнопка "Подтвердить"
    SubmitButton.Name = "SubmitButton"
    SubmitButton.Parent = MainFrame
    SubmitButton.BackgroundColor3 = Color3.fromRGB(46, 204, 113)
    SubmitButton.BorderSizePixel = 0
    SubmitButton.Position = UDim2.new(0.5, 0, 0, 220)
    SubmitButton.AnchorPoint = Vector2.new(0.5, 0)
    SubmitButton.Size = UDim2.new(0, 340, 0, 45)
    SubmitButton.Font = Enum.Font.GothamBold
    SubmitButton.Text = "✓ Подтвердить ключ"
    SubmitButton.TextColor3 = Color3.fromRGB(255, 255, 255)
    SubmitButton.TextSize = 15
    SubmitButton.AutoButtonColor = false
    
    SubmitCorner.CornerRadius = UDim.new(0, 8)
    SubmitCorner.Parent = SubmitButton
    
    -- Статус
    StatusLabel.Name = "StatusLabel"
    StatusLabel.Parent = MainFrame
    StatusLabel.BackgroundTransparency = 1
    StatusLabel.Position = UDim2.new(0, 0, 1, -40)
    StatusLabel.Size = UDim2.new(1, 0, 0, 30)
    StatusLabel.Font = Enum.Font.Gotham
    StatusLabel.Text = "Ожидание ввода ключа..."
    StatusLabel.TextColor3 = Color3.fromRGB(150, 150, 150)
    StatusLabel.TextSize = 12
    
    -- Кнопка закрытия
    CloseButton.Name = "CloseButton"
    CloseButton.Parent = MainFrame
    CloseButton.BackgroundColor3 = Color3.fromRGB(231, 76, 60)
    CloseButton.BorderSizePixel = 0
    CloseButton.Position = UDim2.new(1, -35, 0, 10)
    CloseButton.Size = UDim2.new(0, 25, 0, 25)
    CloseButton.Font = Enum.Font.GothamBold
    CloseButton.Text = "×"
    CloseButton.TextColor3 = Color3.fromRGB(255, 255, 255)
    CloseButton.TextSize = 18
    CloseButton.AutoButtonColor = false
    
    CloseCorner.CornerRadius = UDim.new(0, 6)
    CloseCorner.Parent = CloseButton
    
    -- Анимация появления
    local openTween = TweenService:Create(
        MainFrame,
        TweenInfo.new(0.4, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
        {Size = UDim2.new(0, 420, 0, 310)}
    )
    openTween:Play()
    
    -- Делаем окно перетаскиваемым
    local dragging = false
    local dragInput, mousePos, framePos
    
    MainFrame.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = true
            mousePos = input.Position
            framePos = MainFrame.Position
            
            input.Changed:Connect(function()
                if input.UserInputState == Enum.UserInputState.End then
                    dragging = false
                end
            end)
        end
    end)
    
    MainFrame.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement then
            dragInput = input
        end
    end)
    
    UserInputService.InputChanged:Connect(function(input)
        if input == dragInput and dragging then
            local delta = input.Position - mousePos
            MainFrame.Position = UDim2.new(
                framePos.X.Scale,
                framePos.X.Offset + delta.X,
                framePos.Y.Scale,
                framePos.Y.Offset + delta.Y
            )
        end
    end)
    
    return {
        ScreenGui = ScreenGui,
        MainFrame = MainFrame,
        KeyBox = KeyBox,
        SubmitButton = SubmitButton,
        GetKeyButton = GetKeyButton,
        StatusLabel = StatusLabel,
        CloseButton = CloseButton
    }
end

-- Проверка ключа через API
function KeySystem:VerifyKey(key)
    local success, result = pcall(function()
        local response = game:HttpGet(CONFIG.APIEndpoint .. "?key=" .. key)
        return HttpService:JSONDecode(response)
    end)
    
    if success and result then
        return result.success == true
    end
    
    return false
end

-- Копирование ссылки
function KeySystem:CopyBotLink()
    if setclipboard then
        setclipboard(CONFIG.BotURL)
        return true
    elseif syn and syn.write_clipboard then
        syn.write_clipboard(CONFIG.BotURL)
        return true
    elseif Clipboard and Clipboard.set then
        Clipboard.set(CONFIG.BotURL)
        return true
    end
    return false
end

-- Основная функция
function KeySystem:Init(callback)
    local UI = self:CreateUI()
    
    -- Обработчик "Получить ключ"
    UI.GetKeyButton.MouseButton1Click:Connect(function()
        -- Анимация
        TweenService:Create(
            UI.GetKeyButton,
            TweenInfo.new(0.1),
            {BackgroundColor3 = Color3.fromRGB(41, 128, 185)}
        ):Play()
        
        wait(0.1)
        
        TweenService:Create(
            UI.GetKeyButton,
            TweenInfo.new(0.1),
            {BackgroundColor3 = Color3.fromRGB(52, 152, 219)}
        ):Play()
        
        -- Копирование ссылки
        if self:CopyBotLink() then
            UI.StatusLabel.Text = "✓ Ссылка скопирована! Откройте бота в Telegram"
            UI.StatusLabel.TextColor3 = Color3.fromRGB(46, 204, 113)
        else
            UI.StatusLabel.Text = "Откройте: " .. CONFIG.BotURL
            UI.StatusLabel.TextColor3 = Color3.fromRGB(52, 152, 219)
        end
    end)
    
    -- Hover эффект для GetKeyButton
    UI.GetKeyButton.MouseEnter:Connect(function()
        TweenService:Create(
            UI.GetKeyButton,
            TweenInfo.new(0.2),
            {BackgroundColor3 = Color3.fromRGB(41, 128, 185)}
        ):Play()
    end)
    
    UI.GetKeyButton.MouseLeave:Connect(function()
        TweenService:Create(
            UI.GetKeyButton,
            TweenInfo.new(0.2),
            {BackgroundColor3 = Color3.fromRGB(52, 152, 219)}
        ):Play()
    end)
    
    -- Обработчик "Подтвердить"
    UI.SubmitButton.MouseButton1Click:Connect(function()
        local key = UI.KeyBox.Text
        
        if key == "" or key == " " then
            UI.StatusLabel.Text = "❌ Введите ключ!"
            UI.StatusLabel.TextColor3 = Color3.fromRGB(231, 76, 60)
            return
        end
        
        -- Анимация загрузки
        UI.SubmitButton.Text = "⏳ Проверка..."
        UI.StatusLabel.Text = "Проверка ключа на сервере..."
        UI.StatusLabel.TextColor3 = Color3.fromRGB(241, 196, 15)
        
        -- Проверка ключа
        local isValid = self:VerifyKey(key)
        
        if isValid then
            UI.StatusLabel.Text = "✓ Ключ принят! Загрузка скрипта..."
            UI.StatusLabel.TextColor3 = Color3.fromRGB(46, 204, 113)
            UI.SubmitButton.BackgroundColor3 = Color3.fromRGB(46, 204, 113)
            UI.SubmitButton.Text = "✓ Успешно!"
            
            wait(1)
            
            -- Анимация закрытия
            local closeTween = TweenService:Create(
                UI.MainFrame,
                TweenInfo.new(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.In),
                {Size = UDim2.new(0, 0, 0, 0)}
            )
            closeTween:Play()
            closeTween.Completed:Wait()
            
            UI.ScreenGui:Destroy()
            
            -- Запуск основного скрипта
            if callback then
                callback()
            end
        else
            UI.StatusLabel.Text = "❌ Неверный ключ или ключ уже использован!"
            UI.StatusLabel.TextColor3 = Color3.fromRGB(231, 76, 60)
            UI.SubmitButton.Text = "✓ Подтвердить ключ"
        end
    end)
    
    -- Hover эффект для SubmitButton
    UI.SubmitButton.MouseEnter:Connect(function()
        TweenService:Create(
            UI.SubmitButton,
            TweenInfo.new(0.2),
            {BackgroundColor3 = Color3.fromRGB(39, 174, 96)}
        ):Play()
    end)
    
    UI.SubmitButton.MouseLeave:Connect(function()
        TweenService:Create(
            UI.SubmitButton,
            TweenInfo.new(0.2),
            {BackgroundColor3 = Color3.fromRGB(46, 204, 113)}
        ):Play()
    end)
    
    -- Обработчик закрытия
    UI.CloseButton.MouseButton1Click:Connect(function()
        local closeTween = TweenService:Create(
            UI.MainFrame,
            TweenInfo.new(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.In),
            {Size = UDim2.new(0, 0, 0, 0)}
        )
        closeTween:Play()
        closeTween.Completed:Wait()
        UI.ScreenGui:Destroy()
    end)
    
    -- Hover для CloseButton
    UI.CloseButton.MouseEnter:Connect(function()
        TweenService:Create(
            UI.CloseButton,
            TweenInfo.new(0.2),
            {BackgroundColor3 = Color3.fromRGB(192, 57, 43)}
        ):Play()
    end)
    
    UI.CloseButton.MouseLeave:Connect(function()
        TweenService:Create(
            UI.CloseButton,
            TweenInfo.new(0.2),
            {BackgroundColor3 = Color3.fromRGB(231, 76, 60)}
        ):Play()
    end)
end

-- ========================================
-- ЗАПУСК СИСТЕМЫ КЛЮЧЕЙ
-- ========================================

print("=" .. string.rep("=", 50))
print("🔥 RAV KEY SYSTEM")
print("=" .. string.rep("=", 50))
print("📱 Bot: " .. CONFIG.BotURL)
print("🌐 API: " .. CONFIG.APIEndpoint)
print("=" .. string.rep("=", 50))

KeySystem:Init(function()
    -- ========================================
    -- ЗДЕСЬ ВСТАВЬ СВОЙ ОСНОВНОЙ СКРИПТ!
    -- ========================================
    
    print("✅ Скрипт успешно загружен!")
    
    -- Уведомление
    game.StarterGui:SetCore("SendNotification", {
        Title = "RAV Script";
        Text = "Успешно загружен!";
        Duration = 5;
        Icon = "rbxassetid://6023426923";
    })
    
    -- ПРИМЕР: Твой основной скрипт
    --[[
    
    print("Привет! Ключ работает!")
    
    -- Твой код здесь...
    -- Например:
    -- loadstring(game:HttpGet("https://твой-основной-скрипт.lua"))()
    
    ]]--
    
end)
