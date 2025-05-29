import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/material.dart';

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:5000'; // Altere se for emulador ou dispositivo real

  static Future<void> iniciarConversaComAssistente(BuildContext context) async {
    final url = Uri.parse('$baseUrl/assistente');

    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final resposta = data['resposta'];

        // Mostra a resposta da assistente
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: const Text('CrazIA'),
            content: Text(resposta),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('OK'),
              ),
            ],
          ),
        );
      } else {
        debugPrint("Erro: ${response.statusCode}");
      }
    } catch (e) {
      debugPrint("Erro ao chamar API: $e");
    }
  }
}
