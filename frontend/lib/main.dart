import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'api_voz_service.dart';
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final ValueNotifier<ThemeMode> themeNotifier = ValueNotifier(ThemeMode.light);

  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeNotifier,
      builder: (context, currentTheme, _) {
        return MaterialApp(
          title: 'CrazIA',
          debugShowCheckedModeBanner: false,
          themeMode: currentTheme,
          theme: ThemeData(
            brightness: Brightness.light,
            primarySwatch: Colors.indigo,
            useMaterial3: true,
          ),
          darkTheme: ThemeData(
            brightness: Brightness.dark,
            colorSchemeSeed: Colors.indigo,
            useMaterial3: true,
          ),
          home: HomePage(themeNotifier: themeNotifier),
        );
      },
    );
  }
}

class HomePage extends StatelessWidget {
  final ValueNotifier<ThemeMode> themeNotifier;
  const HomePage({super.key, required this.themeNotifier});

  final String telegramUsername = 'seu_usuario_telegram'; // Substitua com seu @

  void abrirTelegram() async {
    final url = 'https://t.me/$telegramUsername';
    if (await canLaunchUrl(Uri.parse(url))) {
      await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
    } else {
      debugPrint('Não foi possível abrir o Telegram');
    }
  }

void ligarAssistente(BuildContext context) {
  showDialog(
    context: context,
    builder: (_) => const AlertDialog(
      title: Text('Iniciando Assistente'),
      content: Text('Aguarde enquanto a CrazIA inicia a conversa por voz.'),
    ),
  );

  // Espera 1 segundo só para deixar a UI respirar, e então inicia a chamada
  Future.delayed(const Duration(seconds: 1), () {
    Navigator.pop(context); // Fecha o popup de aviso
    ApiService.iniciarConversaComAssistente(context);
  });
}

  @override
  Widget build(BuildContext context) {
    final isDark = themeNotifier.value == ThemeMode.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('CrazIA', style: TextStyle(fontWeight: FontWeight.w600)),
        centerTitle: true,
      ),
      drawer: Drawer(
        child: Column(
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [Colors.indigo, Colors.indigoAccent],
                ),
              ),
              child: const Align(
                alignment: Alignment.bottomLeft,
                child: Text(
                  'CrazIA Menu',
                  style: TextStyle(color: Colors.white, fontSize: 24),
                ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.alarm_outlined),
              title: const Text('Alarmes'),
              onTap: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Alarme clicado!')),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.notifications_none),
              title: const Text('Notificações'),
              onTap: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Notificações clicadas!')),
                );
              },
            ),
            const Divider(),
            SwitchListTile(
              title: const Text('Modo Escuro'),
              value: isDark,
              onChanged: (value) {
                themeNotifier.value = value ? ThemeMode.dark : ThemeMode.light;
              },
              secondary: const Icon(Icons.brightness_6_outlined),
            ),
          ],
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              FilledButton.icon(
                onPressed: abrirTelegram,
                icon: const Icon(Icons.message_outlined),
                label: const Text('Falar via Telegram'),
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(50),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              FilledButton.icon(
                onPressed: () => ligarAssistente(context),
                icon: const Icon(Icons.phone_outlined),
                label: const Text('Ligar para Assistente'),
                style: FilledButton.styleFrom(
                  backgroundColor: Colors.green,
                  foregroundColor: Colors.white,
                  minimumSize: const Size.fromHeight(50),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}