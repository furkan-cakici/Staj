package com.example.fabrikaapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                FabrikaAppContent()
            }
        }
    }
}

// --- 1. UYGULAMA ANA KONTROLCÜSÜ ---
@Composable
fun FabrikaAppContent() {
    var isLoggedIn by remember { mutableStateOf(false) }

    if (isLoggedIn) {
        MainScreen(onLogout = { isLoggedIn = false })
    } else {
        LoginScreen(onLoginSuccess = { isLoggedIn = true })
    }
}

// --- 2. GİRİŞ EKRANI (Güncellenen Kısım) ---
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(onLoginSuccess: () -> Unit) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isError by remember { mutableStateOf(false) } // Hata durumunu takip eden değişken

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF8F9FA))
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(
            imageVector = Icons.Default.Factory,
            contentDescription = "Logo",
            modifier = Modifier.size(80.dp),
            tint = MaterialTheme.colorScheme.primary
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "Fabrika Portalına Hoş Geldiniz",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = Color.DarkGray
        )

        Spacer(modifier = Modifier.height(32.dp))

        // Kullanıcı Adı Giriş Alanı
        OutlinedTextField(
            value = username,
            onValueChange = {
                username = it
                isError = false // Kullanıcı yazmaya başlayınca hatayı sıfırla
            },
            label = { Text("Kullanıcı Adı") },
            placeholder = { Text("") },
            leadingIcon = { Icon(Icons.Default.Person, contentDescription = "Kullanıcı") },
            isError = isError, // Hata varsa alan kırmızı olur
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Şifre Giriş Alanı
        OutlinedTextField(
            value = password,
            onValueChange = {
                password = it
                isError = false // Kullanıcı yazmaya başlayınca hatayı sıfırla
            },
            label = { Text("Şifre") },
            placeholder = { Text("") },
            leadingIcon = { Icon(Icons.Default.Lock, contentDescription = "Şifre") },
            visualTransformation = PasswordVisualTransformation(),
            isError = isError, // Hata varsa alan kırmızı olur
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )

        // Eğer giriş hatalıysa ekranda kırmızı uyarı metni gösterir
        if (isError) {
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Hatalı kullanıcı adı veya şifre!",
                color = Color.Red,
                fontSize = 14.sp,
                modifier = Modifier.align(Alignment.Start)
            )
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Giriş Butonu
        Button(
            onClick = {
                // Sabit kullanıcı adı ve şifre doğrulaması
                if (username == "admin" && password == "1234") {
                    onLoginSuccess() // Başarılıysa ana ekrana geç
                } else {
                    isError = true // Hatalıysa hata durumunu aktif et
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp),
            shape = RoundedCornerShape(8.dp)
        ) {
            Text("Giriş Yap", fontSize = 18.sp)
        }
    }
}

// --- 3. VERİ MODELLERİ VE MOCK VERİLER ---
data class MealMenu(val id: Int, val date: String, val soup: String, val mainCourse: String, val sideDish: String, val dessert: String)
data class Announcement(val id: Int, val title: String, val description: String, val timeAgo: String, val isUrgent: Boolean)

val mockMenus = listOf(
    MealMenu(1, "15 Nisan Salı", "Mercimek Çorbası", "Karnıyarık", "Pirinç Pilavı", "Sütlaç"),
    MealMenu(2, "16 Nisan Çarşamba", "Ezogelin Çorbası", "Tavuk Sote", "Bulgur Pilavı", "Meyve")
)

val mockAnnouncements = listOf(
    Announcement(1, "Bakım Çalışması", "Yarın saat 10:00'da atölye A'da ağ altyapı bakımı olacaktır.", "1 Saat Önce", isUrgent = true),
    Announcement(2, "Yazlık Kıyafet Dağıtımı", "Personel yazlık iş kıyafetlerini depodan teslim alabilir.", "Dün", isUrgent = false)
)

// --- 4. ANA EKRAN VE ALT NAVİGASYON ---
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(onLogout: () -> Unit) {
    var selectedTabIndex by remember { mutableStateOf(0) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (selectedTabIndex == 0) "Yemek Menüsü" else "Duyurular", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = onLogout) {
                        Icon(Icons.Default.ExitToApp, contentDescription = "Çıkış Yap", tint = Color.Red)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        bottomBar = {
            NavigationBar(containerColor = MaterialTheme.colorScheme.surfaceVariant) {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Menu, contentDescription = "Menü") },
                    label = { Text("Menü") },
                    selected = selectedTabIndex == 0,
                    onClick = { selectedTabIndex = 0 }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Notifications, contentDescription = "Duyurular") },
                    label = { Text("Duyurular") },
                    selected = selectedTabIndex == 1,
                    onClick = { selectedTabIndex = 1 }
                )
            }
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            if (selectedTabIndex == 0) MenuScreen() else AnnouncementScreen()
        }
    }
}

// --- 5. YEMEK MENÜSÜ EKRANI ---
@Composable
fun MenuScreen() {
    LazyColumn(
        modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA)),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(mockMenus) { menu ->
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(text = menu.date, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(bottom = 12.dp))
                    Text(text = "🍲 Çorba: ${menu.soup}", fontSize = 16.sp, modifier = Modifier.padding(bottom = 6.dp))
                    Text(text = "🍛 Ana Yemek: ${menu.mainCourse}", fontSize = 16.sp, modifier = Modifier.padding(bottom = 6.dp))
                    Text(text = "🍚 Yan Lezzet: ${menu.sideDish}", fontSize = 16.sp, modifier = Modifier.padding(bottom = 6.dp))
                    Text(text = "🍮 Tatlı: ${menu.dessert}", fontSize = 16.sp)
                }
            }
        }
    }
}

// --- 6. DUYURULAR EKRANI ---
@Composable
fun AnnouncementScreen() {
    LazyColumn(
        modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA)),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(mockAnnouncements) { announcement ->
            val containerColor = if (announcement.isUrgent) Color(0xFFFFF0F0) else Color.White
            val borderColor = if (announcement.isUrgent) Color(0xFFFFCDCD) else Color.Transparent

            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = containerColor),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                border = BorderStroke(1.dp, borderColor),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (announcement.isUrgent) {
                            Icon(Icons.Default.Warning, contentDescription = "Acil", tint = Color.Red)
                            Spacer(modifier = Modifier.width(8.dp))
                        }
                        Text(text = announcement.title, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = if (announcement.isUrgent) Color.Red else Color.Black)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(text = announcement.description, fontSize = 15.sp, color = Color.DarkGray)
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(text = announcement.timeAgo, fontSize = 12.sp, color = Color.Gray)
                }
            }
        }
    }
}