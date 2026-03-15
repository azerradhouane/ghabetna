import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Unified token storage:
/// - Web   → SharedPreferences (secure_storage doesn't work on web)
/// - Mobile → FlutterSecureStorage (encrypted keychain/keystore)

class TokenStorage {
    static const _accessKey='access_token';
    static const _refreshKey='refresh_token';

    static const _secure=FlutterSecureStorage(
        aOptions: AndroidOptions()
    );

    static Future<void> saveTokens(String access,String refresh) async{
        if (kIsWeb){
            final prefs=await SharedPreferences.getInstance();
            await prefs.setString(_accessKey, access);
            await prefs.setString(_refreshKey, refresh);
        }else{
            await _secure.write(key: _accessKey, value: access);
            await _secure.write(key: _refreshKey, value: refresh);
        }
    }

    static Future<String?> getAccessToken() async{
        if(kIsWeb){
            return (await SharedPreferences.getInstance()).getString(_accessKey);
        }
        return _secure.read(key:_accessKey);
    }
    static Future<String?> getRefreshToken() async{
        if(kIsWeb){
            return (await SharedPreferences.getInstance()).getString(_refreshKey);
        }
        return _secure.read(key: _refreshKey);
    }

    static Future<void> clear() async {
        if (kIsWeb){
            final prefs=await SharedPreferences.getInstance();
            await prefs.remove(_accessKey);
            await prefs.remove(_refreshKey);
        }else{
            await _secure.delete(key: _accessKey);
            await _secure.delete(key: _refreshKey);
        }
    }

    static Future<bool> hasToken() async{
        final token=await getAccessToken();
        return token!=null && token.isNotEmpty;
    }
}
