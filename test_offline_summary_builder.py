#!/usr/bin/env python3
"""
Test script to demonstrate the offline summary builder functionality.
"""

import os
import sys
import json
from agents.offline_summary_builder import OfflineSummaryBuilder

def test_single_user_summary():
    """Test generating a comprehensive summary for a single user."""
    print("🧪 Testing Single User Summary Generation")
    print("=" * 50)
    
    try:
        # Initialize the offline summary builder
        builder = OfflineSummaryBuilder(output_dir="user_summaries")
        
        # Test with a specific user
        user_id = "user_001"
        print(f"Generating comprehensive summary for {user_id}...")
        
        # Generate summary
        summary_data = builder.generate_user_summary(user_id)
        
        # Save summary
        filepath = builder.save_user_summary(user_id, summary_data)
        
        print(f"✅ SUCCESS!")
        print(f"Summary saved to: {filepath}")
        print(f"Domains processed: {list(summary_data['domains'].keys())}")
        print(f"Cross-domain insights generated: {'cross_domain_insights' in summary_data}")
        print(f"Overall assessment generated: {'overall_health_assessment' in summary_data}")
        print(f"Comprehensive recommendations generated: {'recommendations' in summary_data}")
        
        # Show a preview of the summary
        print("\n📋 Summary Preview:")
        print("-" * 40)
        if 'overall_health_assessment' in summary_data and 'assessment' in summary_data['overall_health_assessment']:
            assessment = summary_data['overall_health_assessment']['assessment']
            print(assessment[:300] + "..." if len(assessment) > 300 else assessment)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_multiple_users():
    """Test generating summaries for multiple users."""
    print("\n🧪 Testing Multiple Users Summary Generation")
    print("=" * 50)
    
    try:
        # Initialize the offline summary builder
        builder = OfflineSummaryBuilder(output_dir="user_summaries")
        
        # Process all users
        print("Processing all available users...")
        results = builder.process_all_users()
        
        print(f"✅ PROCESSING COMPLETE!")
        print(f"Total users: {results['total_users']}")
        print(f"Successfully processed: {len(results['processed_users'])}")
        print(f"Failed: {len(results['failed_users'])}")
        print(f"Summary files created: {len(results['summary_files'])}")
        
        if results['processed_users']:
            print(f"\nSuccessfully processed users: {', '.join(results['processed_users'])}")
        
        if results['failed_users']:
            print(f"\nFailed users:")
            for failed in results['failed_users']:
                print(f"  - {failed['user_id']}: {failed['error']}")
        
        return len(results['failed_users']) == 0
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_summary_stats():
    """Test getting summary statistics."""
    print("\n🧪 Testing Summary Statistics")
    print("=" * 50)
    
    try:
        # Initialize the offline summary builder
        builder = OfflineSummaryBuilder(output_dir="user_summaries")
        
        # Get statistics
        stats = builder.get_summary_stats()
        
        print(f"✅ STATISTICS RETRIEVED!")
        print(f"Total summaries: {stats['total_summaries']}")
        print(f"Output directory: {stats['output_directory']}")
        print(f"Last updated: {stats['last_updated']}")
        
        if stats['summary_files']:
            print(f"\nSummary files:")
            for filename in stats['summary_files']:
                print(f"  - {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_summary_content():
    """Test reading and displaying summary content."""
    print("\n🧪 Testing Summary Content")
    print("=" * 50)
    
    try:
        # Check if summary files exist
        if not os.path.exists("user_summaries"):
            print("❌ No user_summaries directory found. Run the summary generation first.")
            return False
        
        summary_files = [f for f in os.listdir("user_summaries") if f.endswith('_comprehensive_summary.json')]
        
        if not summary_files:
            print("❌ No summary files found. Run the summary generation first.")
            return False
        
        # Load and display a sample summary
        sample_file = summary_files[0]
        filepath = os.path.join("user_summaries", sample_file)
        
        with open(filepath, 'r') as f:
            summary_data = json.load(f)
        
        print(f"✅ LOADED SUMMARY: {sample_file}")
        print(f"User ID: {summary_data.get('user_id', 'Unknown')}")
        print(f"Generated at: {summary_data.get('generated_at', 'Unknown')}")
        print(f"Domains processed: {list(summary_data.get('domains', {}).keys())}")
        
        # Show domain summaries
        print(f"\n📊 Domain Summaries:")
        for domain, domain_data in summary_data.get('domains', {}).items():
            if 'summary' in domain_data:
                summary = domain_data['summary']
                print(f"\n{domain.upper()}:")
                print(f"  {summary[:200]}..." if len(summary) > 200 else f"  {summary}")
        
        # Show cross-domain insights
        if 'cross_domain_insights' in summary_data and 'insights' in summary_data['cross_domain_insights']:
            insights = summary_data['cross_domain_insights']['insights']
            print(f"\n🔗 Cross-Domain Insights:")
            print(f"  {insights[:300]}..." if len(insights) > 300 else f"  {insights}")
        
        # Show recommendations
        if 'recommendations' in summary_data and 'recommendations' in summary_data['recommendations']:
            recs = summary_data['recommendations']['recommendations']
            print(f"\n💡 Comprehensive Recommendations:")
            print(f"  {recs[:300]}..." if len(recs) > 300 else f"  {recs}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Starting Offline Summary Builder Tests")
    print("=" * 60)
    
    # Test single user summary
    single_success = test_single_user_summary()
    
    # Test multiple users
    multiple_success = test_multiple_users()
    
    # Test summary statistics
    stats_success = test_summary_stats()
    
    # Test summary content
    content_success = test_summary_content()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    results = {
        "Single User Summary": single_success,
        "Multiple Users": multiple_success,
        "Summary Statistics": stats_success,
        "Summary Content": content_success
    }
    
    all_passed = all(results.values())
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("The offline summary builder is working correctly.")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please check the logs for details.")
    
    print(f"\nCheck the user_summaries directory for generated summary files.")
    print(f"Check the testing_logs directory for detailed logs.")

if __name__ == "__main__":
    main() 