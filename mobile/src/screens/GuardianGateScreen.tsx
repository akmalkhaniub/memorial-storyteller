import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert } from 'react-native';

export default function GuardianGateScreen({ navigation }: any) {
  const [pin, setPin] = useState('');
  const [isUnlocked, setIsUnlocked] = useState(false);

  const handleVerifyPin = () => {
    if (pin === '1234') {
      setIsUnlocked(true);
      Alert.alert("Guardian Verified", "You now have access to preview and approve generated videos.");
    } else {
      Alert.alert("Incorrect PIN", "Please enter the correct 4-digit guardian PIN.");
    }
  };

  const handleApproveVideo = () => {
    Alert.alert(
      "Story Approved",
      "This video is now approved and unlocked in the Kids' Story Vault!",
      [{ text: "Go to Kids Vault", onPress: () => navigation.navigate('ChildVault') }]
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🛡️ Guardian Review Gate</Text>
      <Text style={styles.subtitle}>
        Child-Safe Protection: All generated videos must be reviewed and approved by an adult before children can view them.
      </Text>

      {!isUnlocked ? (
        <View style={styles.pinCard}>
          <Text style={styles.pinLabel}>Enter Guardian PIN</Text>
          <TextInput
            style={styles.pinInput}
            value={pin}
            onChangeText={setPin}
            keyboardType="numeric"
            maxLength={4}
            secureTextEntry
            placeholder="••••"
            placeholderTextColor="#64748B"
          />
          <TouchableOpacity style={styles.primaryButton} onPress={handleVerifyPin}>
            <Text style={styles.primaryButtonText}>Unlock Review Mode</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.reviewCard}>
          <View style={styles.videoPlaceholder}>
            <Text style={styles.playIcon}>▶</Text>
            <Text style={styles.videoText}>Preview: "The Starlight Blanket"</Text>
          </View>

          <View style={styles.decisionRow}>
            <TouchableOpacity style={styles.rejectButton} onPress={() => navigation.goBack()}>
              <Text style={styles.rejectButtonText}>Edit Script</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.approveButton} onPress={handleApproveVideo}>
              <Text style={styles.approveButtonText}>Approve for Kids ✓</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A', padding: 20, justifyContent: 'center' },
  title: { fontSize: 22, fontWeight: '700', color: '#F8FAFC', marginBottom: 8, textAlign: 'center' },
  subtitle: { fontSize: 14, color: '#94A3B8', textAlign: 'center', marginBottom: 30, lineHeight: 20 },
  pinCard: { backgroundColor: '#1E293B', padding: 24, borderRadius: 16, alignItems: 'center' },
  pinLabel: { color: '#E2E8F0', fontSize: 16, fontWeight: '600', marginBottom: 12 },
  pinInput: { backgroundColor: '#0F172A', width: 140, height: 50, borderRadius: 12, textAlign: 'center', fontSize: 24, color: '#38BDF8', letterSpacing: 8, marginBottom: 20 },
  primaryButton: { backgroundColor: '#38BDF8', borderRadius: 12, paddingVertical: 14, paddingHorizontal: 24, width: '100%', alignItems: 'center' },
  primaryButtonText: { color: '#0F172A', fontWeight: '700', fontSize: 15 },
  reviewCard: { backgroundColor: '#1E293B', padding: 20, borderRadius: 16 },
  videoPlaceholder: { height: 220, backgroundColor: '#0F172A', borderRadius: 12, justifyContent: 'center', alignItems: 'center', marginBottom: 20 },
  playIcon: { fontSize: 44, color: '#38BDF8', marginBottom: 8 },
  videoText: { color: '#CBD5E1', fontSize: 14 },
  decisionRow: { flexDirection: 'row', gap: 12 },
  rejectButton: { flex: 1, backgroundColor: '#334155', padding: 14, borderRadius: 12, alignItems: 'center' },
  rejectButtonText: { color: '#94A3B8', fontWeight: '600' },
  approveButton: { flex: 1, backgroundColor: '#10B981', padding: 14, borderRadius: 12, alignItems: 'center' },
  approveButtonText: { color: '#FFFFFF', fontWeight: '700' }
});
