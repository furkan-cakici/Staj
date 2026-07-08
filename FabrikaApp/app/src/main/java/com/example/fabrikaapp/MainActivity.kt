package com.example.fabrikaapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
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
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.fabrikaapp.R
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

// --- ÖZEL FONT ---
val ElectromagneticLungs = FontFamily(
    Font(R.font.electromagnetic_lungs)
)

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

data class MealMenu(val id: Int, val date: String, val soup: String, val mainCourse: String, val sideDish: String, val dessert: String)
data class Announcement(val id: Int, val title: String, val description: String, val timeAgo: String, val isUrgent: Boolean)

// --- RETROFIT NETWORK KATMANI ---
interface ApiService {
    @GET("api/menu")
    suspend fun getMenu(): List<MealMenu>

    @GET("api/announcements")
    suspend fun getAnnouncements(): List<Announcement>
}

object RetrofitClient {
    // BURAYA RENDER'IN SANA VERDİĞİ LİNKİ YAPIŞTIR (Sonunda / işareti olmasına dikkat et)
    private const val BASE_URL = "https://fabrika-api.onrender.com/"

    val instance: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}

// --- UYGULAMA ANA KONTROLCÜSÜ ---
@Composable
fun FabrikaAppContent() {
    var isLoggedIn by remember { mutableStateOf(false) }

    if (isLoggedIn) {
        MainScreen(onLogout = { isLoggedIn = false })
    } else {
        LoginScreen(onLoginSuccess = { isLoggedIn = true })
    }
}

// --- GİRİŞ EKRANI ---
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(onLoginSuccess: () -> Unit) {
    val isDark = isSystemInDarkTheme()

    // Gece/Gündüz Renk Değişkenleri
    val bgColor = if (isDark) Color.Black else Color.White
    val textColor = if (isDark) Color.White else Color.Black
    val textSecColor = if (isDark) Color.LightGray else Color.DarkGray

    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isError by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {

        Text(
            text = "bien",
            fontFamily = ElectromagneticLungs,
            fontSize = 80.sp,
            color = textColor,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        Text(
            text = "Kurumsal Portala Hoş Geldiniz",
            fontSize = 20.sp,
            fontWeight = FontWeight.Medium,
            color = textSecColor
        )

        Spacer(modifier = Modifier.height(40.dp))

        OutlinedTextField(
            value = username,
            onValueChange = {
                username = it
                isError = false
            },
            label = { Text("Kullanıcı Adı") },
            leadingIcon = { Icon(Icons.Default.Person, contentDescription = "Kullanıcı") },
            isError = isError,
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = textColor,
                unfocusedBorderColor = Color.Gray,
                cursorColor = textColor,
                focusedTextColor = textColor,
                unfocusedTextColor = textColor,
                focusedLeadingIconColor = textColor,
                unfocusedLeadingIconColor = Color.Gray,
                focusedLabelColor = textColor,
                unfocusedLabelColor = Color.Gray
            )
        )

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = password,
            onValueChange = {
                password = it
                isError = false
            },
            label = { Text("Şifre") },
            leadingIcon = { Icon(Icons.Default.Lock, contentDescription = "Şifre") },
            visualTransformation = PasswordVisualTransformation(),
            isError = isError,
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = textColor,
                unfocusedBorderColor = Color.Gray,
                cursorColor = textColor,
                focusedTextColor = textColor,
                unfocusedTextColor = textColor,
                focusedLeadingIconColor = textColor,
                unfocusedLeadingIconColor = Color.Gray,
                focusedLabelColor = textColor,
                unfocusedLabelColor = Color.Gray
            )
        )

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

        Button(
            onClick = {
                if (username == "admin" && password == "1234") {
                    onLoginSuccess()
                } else {
                    isError = true
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp),
            shape = RoundedCornerShape(8.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = textColor, // Buton arka planı (Karanlıkta beyaz, aydınlıkta siyah)
                contentColor = bgColor      // Buton yazısı (Karanlıkta siyah, aydınlıkta beyaz)
            )
        ) {
            Text("Giriş Yap", fontSize = 18.sp, fontWeight = FontWeight.Bold)
        }
    }
}

// --- ANA EKRAN VE ALT NAVİGASYON ---
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(onLogout: () -> Unit) {
    val isDark = isSystemInDarkTheme()
    val bgColor = if (isDark) Color.Black else Color.White
    val textColor = if (isDark) Color.White else Color.Black

    var selectedTabIndex by remember { mutableStateOf(0) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (selectedTabIndex == 0) "Yemek Menüsü" else "Duyurular", fontWeight = FontWeight.Bold, color = textColor) },
                actions = {
                    IconButton(onClick = onLogout) {
                        Icon(Icons.Default.ExitToApp, contentDescription = "Çıkış Yap", tint = Color.Gray)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
            )
        },
        bottomBar = {
            NavigationBar(
                containerColor = bgColor,
                tonalElevation = 8.dp
            ) {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.RestaurantMenu, contentDescription = "Yemek Menüsü") },
                    label = { Text("Yemek Menüsü") },
                    selected = selectedTabIndex == 0,
                    onClick = { selectedTabIndex = 0 },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = bgColor,
                        selectedTextColor = textColor,
                        indicatorColor = textColor,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Notifications, contentDescription = "Duyurular") },
                    label = { Text("Duyurular") },
                    selected = selectedTabIndex == 1,
                    onClick = { selectedTabIndex = 1 },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = bgColor,
                        selectedTextColor = textColor,
                        indicatorColor = textColor,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
            }
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            if (selectedTabIndex == 0) MenuScreen() else AnnouncementScreen()
        }
    }
}

// --- DINAMIK YEMEK MENÜSÜ EKRANI ---
@Composable
fun MenuScreen() {
    val isDark = isSystemInDarkTheme()
    val bgPrimary = if (isDark) Color.Black else Color(0xFFF8F9FA)
    val cardSurface = if (isDark) Color(0xFF121212) else Color.White
    val textColor = if (isDark) Color.White else Color.Black
    val textSecColor = if (isDark) Color.LightGray else Color.DarkGray
    val borderColor = if (isDark) Color(0xFF333333) else Color(0xFFEEEEEE)

    var menuList by remember { mutableStateOf<List<MealMenu>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        try {
            menuList = RetrofitClient.instance.getMenu()
        } catch (e: Exception) {
        } finally {
            isLoading = false
        }
    }

    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize().background(bgPrimary), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = textColor)
        }
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize().background(bgPrimary),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(menuList) { menu ->
                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = cardSurface),
                    elevation = CardDefaults.cardElevation(defaultElevation = 0.5.dp),
                    border = BorderStroke(1.dp, borderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(text = menu.date, fontWeight = FontWeight.Bold, color = textColor, modifier = Modifier.padding(bottom = 12.dp))
                        Text(text = "🍲 Çorba: ${menu.soup}", fontSize = 16.sp, color = textSecColor, modifier = Modifier.padding(bottom = 6.dp))
                        Text(text = "🍛 Ana Yemek: ${menu.mainCourse}", fontSize = 16.sp, color = textSecColor, modifier = Modifier.padding(bottom = 6.dp))
                        Text(text = "🍚 Yan Lezzet: ${menu.sideDish}", fontSize = 16.sp, color = textSecColor, modifier = Modifier.padding(bottom = 6.dp))
                        Text(text = "🍮 Tatlı: ${menu.dessert}", fontSize = 16.sp, color = textSecColor)
                    }
                }
            }
        }
    }
}

// --- DINAMIK DUYURULAR EKRANI ---
@Composable
fun AnnouncementScreen() {
    val isDark = isSystemInDarkTheme()
    val bgPrimary = if (isDark) Color.Black else Color(0xFFF8F9FA)
    val cardSurface = if (isDark) Color(0xFF121212) else Color.White
    val textColor = if (isDark) Color.White else Color.Black
    val textSecColor = if (isDark) Color.LightGray else Color.DarkGray
    val borderColor = if (isDark) Color(0xFF333333) else Color(0xFFEEEEEE)

    // Acil durum kartları için karanlık mod renkleri
    val urgentBgDark = Color(0xFF3B1111)
    val urgentBorderDark = Color(0xFF8A2121)

    var announcementList by remember { mutableStateOf<List<Announcement>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        try {
            announcementList = RetrofitClient.instance.getAnnouncements()
        } catch (e: Exception) {
        } finally {
            isLoading = false
        }
    }

    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize().background(bgPrimary), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = textColor)
        }
    } else if (announcementList.isEmpty()) {
        Box(
            modifier = Modifier.fillMaxSize().background(bgPrimary),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "Duyuru bulunmamaktadır.",
                fontSize = 16.sp,
                color = Color.Gray,
                fontWeight = FontWeight.Medium
            )
        }
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize().background(bgPrimary),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(announcementList) { announcement ->
                val containerColor = if (announcement.isUrgent) {
                    if (isDark) urgentBgDark else Color(0xFFFFF0F0)
                } else cardSurface

                val currentBorderColor = if (announcement.isUrgent) {
                    if (isDark) urgentBorderDark else Color(0xFFFFCDCD)
                } else borderColor

                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = containerColor),
                    elevation = CardDefaults.cardElevation(defaultElevation = 0.5.dp),
                    border = BorderStroke(1.dp, currentBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            if (announcement.isUrgent) {
                                Icon(Icons.Default.Warning, contentDescription = "Acil", tint = Color.Red)
                                Spacer(modifier = Modifier.width(8.dp))
                            }
                            Text(text = announcement.title, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = if (announcement.isUrgent) Color.Red else textColor)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(text = announcement.description, fontSize = 15.sp, color = textSecColor)
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(text = announcement.timeAgo, fontSize = 12.sp, color = Color.Gray)
                    }
                }
            }
        }
    }
}