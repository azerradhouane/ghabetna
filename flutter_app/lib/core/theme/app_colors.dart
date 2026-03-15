import 'package:flutter/material.dart';

class AppColors {
    AppColors._();

    // Brand
  static const Color primaryGreen   = Color(0xFF00964B);
  static const Color sage           = Color(0xFF7CB342);
  static const Color teal           = Color(0xFF26A69A);
  static const Color darkForest     = Color(0xFF1B5E20);

  // Semantic
  static const Color success        = Color(0xFF4CAF50);
  static const Color warning        = Color(0xFFFFC107);
  static const Color danger         = Color(0xFFE53935);
  static const Color info           = Color(0xFF2196F3);

  // Light backgrounds
  static const Color lightBg        = Color(0xFFF8FAF8);
  static const Color lightSurface   = Colors.white;
  static const Color lightBorder    = Color(0xFFE8F0E8);

  // Dark backgrounds
  static const Color darkBg         = Color(0xFF111827);
  static const Color darkSurface    = Color(0xFF1F2937);
  static const Color darkBorder     = Color(0xFF374151);

  // Gradient
  static const LinearGradient primaryGradient=LinearGradient(
    colors: [primaryGreen,teal],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight
    );

    //sidebar
    static const Color sidebarBg=Color(0xFF0D1F12);
    static const Color sidebarActive=Color(0xFF00964B);
    static const Color sidebarText=Color(0xFFD1FAE5);

}
