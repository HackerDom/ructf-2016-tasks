using System;
using System.Collections.Generic;
using System.Linq;
using ApprovalTests.Namers;
using NUnit.Framework;

namespace winme
{
	[TestFixture]
	class FlagGenerationTest
	{
		[Test]
		[TestCase("foo", "bar", "Monday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("foo", "another", "Monday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("foo", "bar", "Sunday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("foo", "another", "Sunday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("1234567890", "bar", "Monday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("1234567890", "another", "Monday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("1234567890", "bar", "Sunday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		public void ImportantParametersTest(string playersId, string appName, string today, string appVersion, string os,
			int processorCount, bool is64BitOperatingSystem, string machineName)
		{
			var results = new List<string>();
			byte[] rightPart;
			using (ApprovalResults.ForScenario(playersId, appName, today, appVersion, os, processorCount, is64BitOperatingSystem, machineName))
			{
				var res = Program.ConfuseEm(playersId, appName, today, new Version(appVersion), os, processorCount,
					is64BitOperatingSystem, machineName, out rightPart);
				results.Add(BitConverter.ToString(res));
				Console.WriteLine(res);
			}
			Assert.False(results.GroupBy(s => s).Any(r => r.Count() > 1));
		}

		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 8, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 8, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 8, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 1, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 1, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 1, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 1, true, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 8, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 8, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 8, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 8, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 1, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 1, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 1, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 1, false, "mycomp")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 8, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 8, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 8, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 8, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 1, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 1, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 1, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 1, true, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 8, false, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 8, false, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 8, false, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 8, false, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Ubuntu", 1, false, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Ubuntu", 1, false, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "1.2.3", "Windows", 1, false, "NJ00DW6")]
		[TestCase("1234567890", "another", "Sunday", "2.2.3", "Windows", 1, false, "NJ00DW6")]
		public void MeaninlessParametersTest(string playersId, string appName, string today, string appVersion, string os,
			int processorCount, bool is64BitOperatingSystem, string machineName)
		{
			var results = new List<string>();
			byte[] rightPart;
			using (ApprovalResults.ForScenario(playersId, appName, today, appVersion, os, processorCount, is64BitOperatingSystem, machineName))
			{
				var res = Program.ConfuseEm(playersId, appName, today, new Version(appVersion), os, processorCount,
					is64BitOperatingSystem, machineName, out rightPart);
				results.Add(BitConverter.ToString(res));
				Console.WriteLine(res);
			}
			Assert.True(results.GroupBy(s => s).Count() == 1);
		}

		[Test]
		public void XorTest()
		{
			var b1 = new byte[1000];
			var b2 = new byte[1000];
			var r = new Random();
			r.NextBytes(b1);
			r.NextBytes(b2);
			var res1 = Program.Xor(b1, b1);
			Assert.True(res1.All(b => b == 0));

			var res2 = Program.Xor(Program.Xor(b1, b2), b2);
			Assert.True(AreEqual(b1, res2));

		}

		bool AreEqual(byte[] b1, byte[] b2)
		{
			if (b1.Length != b2.Length) return false;
			
			for (int i = 0; i < b1.Length; i++)
			{
				if (b1[i] != b2[i]) return false;
			}
			return true;
		}
	}
}
